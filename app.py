from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from database import init_db_pool, close_db_pool, Todo, GroceryItem, ActivityLog
from gmail_service import (
    get_gmail_auth_url, 
    handle_oauth_callback, 
    sync_gmail_messages,
    get_cached_emails,
    is_authenticated
)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for API access
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8080",  # Flask dev server
            os.environ.get('FRONTEND_URL', 'https://yourdomain.com')  # Production
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://matt@localhost:5432/daily_discover')
GMAIL_REDIRECT_URI = os.environ.get('GMAIL_REDIRECT_URI', 'http://localhost:8080/oauth2callback')

# Initialize database connection pool
init_db_pool(DATABASE_URL)

# For demo purposes, use a default user ID (in production, this would come from authentication)
DEFAULT_USER_ID = '00000000-0000-0000-0000-000000000001'

# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def index():
    """Redirect to dashboard or show info page"""
    return """
    <html>
    <head><title>Daily Discover</title></head>
    <body style="font-family: system-ui; max-width: 600px; margin: 50px auto; padding: 20px;">
        <h1>Daily Discover</h1>
        <ul>
            <li><a href="/dashboard">Dashboard</a> (protected)</li>
            <li><a href="/api/health">API Health Check</a></li>
            <li><a href="https://gremlin.computer">Blog</a> (hosted on Cloudflare Pages)</li>
        </ul>
    </body>
    </html>
    """

@app.route('/dashboard')
def dashboard():
    """Protected dashboard page - secure via Cloudflare"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Daily Discover server is running',
        'database': 'connected'
    })

@app.route('/api/groceries', methods=['GET', 'POST'])
def groceries():
    """Handle grocery list operations"""
    try:
        if request.method == 'POST':
            data = request.json
            item_name = data.get('item_name') or data.get('text') or data.get('item')
            quantity = data.get('quantity', 1)
            notes = data.get('notes')
            
            if not item_name:
                return jsonify({'success': False, 'message': 'Item name is required'}), 400
            
            # Create grocery item
            item = GroceryItem.create(DEFAULT_USER_ID, item_name, quantity, notes)
            
            # Log the activity
            ActivityLog.log(
                DEFAULT_USER_ID,
                'grocery_added',
                'grocery',
                str(item['id']),
                {'item_name': item_name, 'quantity': quantity},
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            
            return jsonify({
                'success': True,
                'message': 'Grocery item added',
                'data': item
            }), 201
        else:
            # Get all active grocery items
            items = GroceryItem.get_active(DEFAULT_USER_ID)
            return jsonify({
                'success': True,
                'items': items
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/todos', methods=['GET', 'POST'])
def todos():
    """Handle TODO list operations"""
    try:
        if request.method == 'POST':
            data = request.json
            text = data.get('text')
            priority = data.get('priority', 0)
            
            if not text:
                return jsonify({'success': False, 'message': 'Text is required'}), 400
            
            # Create TODO item
            todo = Todo.create(DEFAULT_USER_ID, text, priority)
            
            # Log the activity
            ActivityLog.log(
                DEFAULT_USER_ID,
                'todo_added',
                'todo',
                str(todo['id']),
                {'text': text, 'priority': priority},
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            
            return jsonify({
                'success': True,
                'message': 'TODO item added',
                'data': todo
            }), 201
        else:
            # Get all incomplete TODOs
            items = Todo.get_all(DEFAULT_USER_ID, include_completed=False)
            return jsonify({
                'success': True,
                'items': items
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/todos/<todo_id>/complete', methods=['POST'])
def complete_todo(todo_id):
    """Mark a TODO as completed"""
    try:
        success = Todo.mark_completed(todo_id, True)
        if success:
            ActivityLog.log(
                DEFAULT_USER_ID,
                'todo_completed',
                'todo',
                todo_id,
                None,
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            return jsonify({'success': True, 'message': 'TODO marked as completed'})
        else:
            return jsonify({'success': False, 'message': 'TODO not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/voice-input', methods=['POST'])
def voice_input():
    """Handle voice input from iOS Shortcuts"""
    try:
        data = request.json
        input_type = data.get('type')
        
        if input_type == 'grocery':
            # Handle single grocery item
            item_name = data.get('item')
            quantity = data.get('quantity', 1)
            
            item = GroceryItem.create(DEFAULT_USER_ID, item_name, quantity)
            ActivityLog.log(
                DEFAULT_USER_ID,
                'grocery_added_voice',
                'grocery',
                str(item['id']),
                {'item_name': item_name, 'source': 'voice'},
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            
            return jsonify({
                'success': True,
                'message': f'Added {item_name} to grocery list'
            })
            
        elif input_type == 'groceries':
            # Handle multiple grocery items
            items = data.get('items', [])
            added_items = []
            
            for item_name in items:
                item = GroceryItem.create(DEFAULT_USER_ID, item_name, 1)
                added_items.append(item)
            
            ActivityLog.log(
                DEFAULT_USER_ID,
                'groceries_added_voice',
                'grocery',
                None,
                {'count': len(items), 'source': 'voice'},
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            
            return jsonify({
                'success': True,
                'message': f'Added {len(items)} items to grocery list',
                'items': added_items
            })
            
        elif input_type == 'todo':
            # Handle TODO item from voice
            text = data.get('text')
            priority = data.get('priority', 0)
            
            todo = Todo.create(DEFAULT_USER_ID, text, priority)
            ActivityLog.log(
                DEFAULT_USER_ID,
                'todo_added_voice',
                'todo',
                str(todo['id']),
                {'text': text, 'source': 'voice'},
                request.remote_addr,
                request.headers.get('User-Agent')
            )
            
            return jsonify({
                'success': True,
                'message': f'Added TODO: {text}'
            })
            
        else:
            return jsonify({
                'success': False,
                'message': 'Unknown input type'
            }), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Gmail API endpoints

@app.route('/api/gmail/auth')
def gmail_auth():
    """Initiate Gmail OAuth flow"""
    auth_url = get_gmail_auth_url(GMAIL_REDIRECT_URI)
    return jsonify({'auth_url': auth_url})

@app.route('/oauth2callback')
def oauth2callback():
    """Handle OAuth2 callback from Google"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f"<h1>Authentication Error</h1><p>{error}</p><a href='/'>Go back to dashboard</a>"
    
    if code:
        try:
            handle_oauth_callback(code, GMAIL_REDIRECT_URI)
            # Immediately sync emails after authentication
            sync_result = sync_gmail_messages(DEFAULT_USER_ID, days_back=20)
            return f"""
                <h1>✅ Gmail Connected!</h1>
                <p>Synced {sync_result.get('synced', 0)} messages ({sync_result.get('new', 0)} new)</p>
                <p><a href="/">Go back to dashboard</a></p>
                <script>setTimeout(() => window.location.href = '/', 2000);</script>
            """
        except Exception as e:
            return f"<h1>Error</h1><p>{str(e)}</p><a href='/'>Go back to dashboard</a>"
    
    return redirect('/')

@app.route('/api/gmail/status')
def gmail_status():
    """Check Gmail authentication status"""
    authenticated = is_authenticated()
    return jsonify({
        'authenticated': authenticated,
        'message': 'Gmail is connected' if authenticated else 'Gmail not connected'
    })

@app.route('/api/gmail/sync', methods=['POST'])
def gmail_sync():
    """Manually sync Gmail messages"""
    if not is_authenticated():
        return jsonify({
            'success': False,
            'error': 'Not authenticated. Please connect Gmail first.'
        }), 401
    
    days_back = request.json.get('days_back', 20) if request.json else 20
    result = sync_gmail_messages(DEFAULT_USER_ID, days_back=days_back)
    
    if result['success']:
        ActivityLog.log(
            DEFAULT_USER_ID,
            'gmail_synced',
            'email',
            None,
            {'synced': result['synced'], 'new': result['new']},
            request.remote_addr,
            request.headers.get('User-Agent')
        )
    
    return jsonify(result)

@app.route('/api/emails')
def get_emails():
    """Get cached email messages"""
    days_back = request.args.get('days_back', 20, type=int)
    unread_only = request.args.get('unread_only', 'true').lower() == 'true'
    
    try:
        emails = get_cached_emails(DEFAULT_USER_ID, days_back=days_back, unread_only=unread_only)
        return jsonify({
            'success': True,
            'emails': emails,
            'count': len(emails)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Blog routes
# ============================================================================
# BLOG API ENDPOINTS - Removed (Blog is static via Pelican)
# Blog content is served directly from / and /blog/* routes above
# ============================================================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True
    )
