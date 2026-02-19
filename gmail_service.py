"""
Gmail API integration for Daily Discover
"""
import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from database import get_db_cursor
import psycopg

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Token storage file
TOKEN_FILE = 'token.pickle'


def get_gmail_auth_url(redirect_uri: str) -> str:
    """Generate Gmail OAuth authorization URL"""
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    return auth_url


def handle_oauth_callback(code: str, redirect_uri: str) -> Credentials:
    """Handle OAuth callback and exchange code for credentials"""
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Save credentials to file
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(credentials, token)
    
    return credentials


def get_credentials() -> Optional[Credentials]:
    """Get stored credentials if they exist and are valid"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh credentials if expired
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed credentials
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            return None
    
    return creds if creds and creds.valid else None


def sync_gmail_messages(user_id: str, days_back: int = 20) -> Dict[str, Any]:
    """
    Sync Gmail messages from the last N days
    Returns summary of synced messages
    """
    creds = get_credentials()
    if not creds:
        return {'success': False, 'error': 'Not authenticated'}
    
    try:
        # Build Gmail service
        service = build('gmail', 'v1', credentials=creds)
        
        # Calculate date filter
        after_date = datetime.now() - timedelta(days=days_back)
        query = f'is:unread after:{after_date.strftime("%Y/%m/%d")}'
        
        # Fetch messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=100
        ).execute()
        
        messages = results.get('messages', [])
        synced_count = 0
        new_count = 0
        
        for msg in messages:
            # Get full message details
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()
            
            # Extract metadata
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            
            gmail_id = message['id']
            thread_id = message['threadId']
            subject = headers.get('Subject', '(No Subject)')
            sender = headers.get('From', '')
            recipient = headers.get('To', '')
            snippet = message.get('snippet', '')
            labels = message.get('labelIds', [])
            
            # Parse date
            date_str = headers.get('Date', '')
            try:
                received_at = datetime.strptime(date_str.split(' (')[0], '%a, %d %b %Y %H:%M:%S %z')
            except:
                received_at = datetime.now()
            
            is_unread = 'UNREAD' in labels
            
            # Insert or update in database
            with get_db_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO email_cache 
                    (user_id, gmail_id, thread_id, subject, sender, recipient, snippet, is_unread, received_at, labels)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (gmail_id) DO UPDATE SET
                        is_unread = EXCLUDED.is_unread,
                        labels = EXCLUDED.labels,
                        synced_at = CURRENT_TIMESTAMP
                    RETURNING (xmax = 0) AS inserted
                    """,
                    (user_id, gmail_id, thread_id, subject, sender, recipient, 
                     snippet, is_unread, received_at, labels)
                )
                result = cursor.fetchone()
                if result['inserted']:
                    new_count += 1
                synced_count += 1
        
        return {
            'success': True,
            'synced': synced_count,
            'new': new_count,
            'total_messages': len(messages)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_cached_emails(user_id: str, days_back: int = 20, unread_only: bool = True) -> List[Dict[str, Any]]:
    """
    Get cached email messages from database
    """
    with get_db_cursor() as cursor:
        after_date = datetime.now() - timedelta(days=days_back)
        
        if unread_only:
            cursor.execute(
                """
                SELECT * FROM email_cache
                WHERE user_id = %s 
                AND received_at >= %s
                AND is_unread = TRUE
                ORDER BY received_at DESC
                LIMIT 50
                """,
                (user_id, after_date)
            )
        else:
            cursor.execute(
                """
                SELECT * FROM email_cache
                WHERE user_id = %s 
                AND received_at >= %s
                ORDER BY received_at DESC
                LIMIT 50
                """,
                (user_id, after_date)
            )
        
        return [dict(row) for row in cursor.fetchall()]


def is_authenticated() -> bool:
    """Check if Gmail is authenticated"""
    creds = get_credentials()
    return creds is not None
