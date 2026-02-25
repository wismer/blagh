"""
Blog service for parsing markdown posts with Jekyll-style front matter
"""
import os
import markdown
import frontmatter
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from database import get_db_cursor

POSTS_DIR = Path(__file__).parent / 'posts'

def scan_and_sync_posts(user_id: str) -> int:
    """
    Scan posts/ directory and sync with database
    Returns number of posts synced
    """
    if not POSTS_DIR.exists():
        return 0
    
    synced_count = 0
    
    for md_file in POSTS_DIR.glob('*.md'):
        if md_file.name == 'README.md':
            continue
            
        try:
            post = frontmatter.load(md_file)
            
            # Skip drafts (unpublished posts)
            if not post.get('published', False):
                continue
            
            # Extract metadata
            slug = post.get('slug', md_file.stem)
            title = post.get('title', slug)
            excerpt = post.get('excerpt', '')
            tags = post.get('tags', [])
            date_str = post.get('date')
            
            # Parse date
            if isinstance(date_str, str):
                published_at = datetime.fromisoformat(date_str)
            elif isinstance(date_str, datetime):
                published_at = date_str
            else:
                published_at = datetime.now()
            
            # Get relative file path
            file_path = md_file.name
            
            # Upsert to database
            with get_db_cursor() as cur:
                cur.execute("""
                    INSERT INTO blog_posts (user_id, slug, title, excerpt, file_path, published_at, is_draft, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (slug) DO UPDATE SET
                        title = EXCLUDED.title,
                        excerpt = EXCLUDED.excerpt,
                        file_path = EXCLUDED.file_path,
                        published_at = EXCLUDED.published_at,
                        is_draft = EXCLUDED.is_draft,
                        tags = EXCLUDED.tags,
                        updated_at = CURRENT_TIMESTAMP
                """, (user_id, slug, title, excerpt, file_path, published_at, False, tags))
            
            synced_count += 1
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            continue
    
    return synced_count


def get_all_posts(user_id: str, include_drafts: bool = False) -> List[Dict]:
    """
    Get all blog posts for a user, sorted by published date (newest first)
    """
    with get_db_cursor() as cur:
        if include_drafts:
            cur.execute("""
                SELECT id, slug, title, excerpt, published_at, is_draft, tags, created_at, updated_at
                FROM blog_posts
                WHERE user_id = %s
                ORDER BY published_at DESC NULLS LAST
            """, (user_id,))
        else:
            cur.execute("""
                SELECT id, slug, title, excerpt, published_at, is_draft, tags, created_at, updated_at
                FROM blog_posts
                WHERE user_id = %s AND is_draft = FALSE
                ORDER BY published_at DESC
            """, (user_id,))
        
        posts = []
        for row in cur.fetchall():
            posts.append({
                'id': str(row['id']),
                'slug': row['slug'],
                'title': row['title'],
                'excerpt': row['excerpt'],
                'published_at': row['published_at'].isoformat() if row['published_at'] else None,
                'is_draft': row['is_draft'],
                'tags': row['tags'] or [],
                'created_at': row['created_at'].isoformat(),
                'updated_at': row['updated_at'].isoformat()
            })
        
        return posts


def get_post_by_slug(user_id: str, slug: str) -> Optional[Dict]:
    """
    Get a single blog post by slug, including rendered HTML content
    """
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT id, slug, title, excerpt, file_path, published_at, is_draft, tags, created_at, updated_at
            FROM blog_posts
            WHERE user_id = %s AND slug = %s
        """, (user_id, slug))
        
        row = cur.fetchone()
        if not row:
            return None
        
        # Load and render markdown content
        md_file = POSTS_DIR / row['file_path']
        if not md_file.exists():
            return None
        
        try:
            post = frontmatter.load(md_file)
            
            # Render markdown to HTML
            md = markdown.Markdown(extensions=[
                'extra',           # Tables, fenced code blocks, etc.
                'codehilite',      # Syntax highlighting
                'toc',             # Table of contents
                'nl2br',           # Newlines to <br>
                'sane_lists'       # Better list handling
            ])
            html_content = md.convert(post.content)
            
            return {
                'id': str(row['id']),
                'slug': row['slug'],
                'title': row['title'],
                'excerpt': row['excerpt'],
                'content': html_content,
                'published_at': row['published_at'].isoformat() if row['published_at'] else None,
                'is_draft': row['is_draft'],
                'tags': row['tags'] or [],
                'created_at': row['created_at'].isoformat(),
                'updated_at': row['updated_at'].isoformat()
            }
        except Exception as e:
            print(f"Error rendering post {slug}: {e}")
            return None


def get_posts_by_tag(user_id: str, tag: str) -> List[Dict]:
    """
    Get all posts with a specific tag
    """
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT id, slug, title, excerpt, published_at, is_draft, tags, created_at, updated_at
            FROM blog_posts
            WHERE user_id = %s AND is_draft = FALSE AND %s = ANY(tags)
            ORDER BY published_at DESC
        """, (user_id, tag))
        
        posts = []
        for row in cur.fetchall():
            posts.append({
                'id': str(row['id']),
                'slug': row['slug'],
                'title': row['title'],
                'excerpt': row['excerpt'],
                'published_at': row['published_at'].isoformat() if row['published_at'] else None,
                'is_draft': row['is_draft'],
                'tags': row['tags'] or [],
                'created_at': row['created_at'].isoformat(),
                'updated_at': row['updated_at'].isoformat()
            })
        
        return posts


def get_all_tags(user_id: str) -> List[str]:
    """
    Get all unique tags used across all posts
    """
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT DISTINCT unnest(tags) as tag
            FROM blog_posts
            WHERE user_id = %s AND is_draft = FALSE
            ORDER BY tag
        """, (user_id,))
        
        return [row['tag'] for row in cur.fetchall()]
