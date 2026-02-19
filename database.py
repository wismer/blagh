"""
Database models and connection management for Daily Discover
"""
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

# Database connection pool
_pool: Optional[ConnectionPool] = None

def init_db_pool(database_url: str, min_size: int = 1, max_size: int = 10):
    """Initialize the database connection pool"""
    global _pool
    if _pool is not None:
        try:
            _pool.close()
        except:
            print("wtf")
    _pool = ConnectionPool(database_url, min_size=min_size, max_size=max_size, open=True)

def get_db_pool() -> ConnectionPool:
    """Get the database connection pool"""
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call init_db_pool() first.")
    return _pool

def close_db_pool():
    """Close the database connection pool"""
    global _pool
    if _pool:
        _pool.close()
        _pool = None

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    pool = get_db_pool()
    with pool.connection() as conn:
        yield conn

@contextmanager
def get_db_cursor():
    """Context manager for database cursors"""
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            yield cursor


class User:
    """User model"""
    
    @staticmethod
    def create(username: str, email: str, password_hash: str) -> Dict[str, Any]:
        """Create a new user"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, username, email, created_at
                """,
                (username, email, password_hash)
            )
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT id, username, email, created_at, updated_at FROM users WHERE id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None


class Todo:
    """TODO item model"""
    
    @staticmethod
    def create(user_id: str, text: str, priority: int = 0) -> Dict[str, Any]:
        """Create a new TODO item"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO todos (user_id, text, priority)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, text, completed, priority, created_at
                """,
                (user_id, text, priority)
            )
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_all(user_id: str, include_completed: bool = False) -> List[Dict[str, Any]]:
        """Get all TODO items for a user"""
        with get_db_cursor() as cursor:
            if include_completed:
                cursor.execute(
                    """
                    SELECT * FROM todos 
                    WHERE user_id = %s 
                    ORDER BY priority DESC, created_at DESC
                    """,
                    (user_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM todos 
                    WHERE user_id = %s AND completed = FALSE
                    ORDER BY priority DESC, created_at DESC
                    """,
                    (user_id,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def mark_completed(todo_id: str, completed: bool = True) -> bool:
        """Mark a TODO as completed or uncompleted"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                UPDATE todos 
                SET completed = %s, 
                    completed_at = CASE WHEN %s THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE id = %s
                """,
                (completed, completed, todo_id)
            )
            return cursor.rowcount > 0


class GroceryItem:
    """Grocery item model"""
    
    @staticmethod
    def create(user_id: str, item_name: str, quantity: int = 1, notes: Optional[str] = None) -> Dict[str, Any]:
        """Create a new grocery item"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO grocery_items (user_id, item_name, quantity, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, item_name, quantity, notes, is_active, created_at
                """,
                (user_id, item_name, quantity, notes)
            )
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_active(user_id: str) -> List[Dict[str, Any]]:
        """Get all active grocery items for a user"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM grocery_items 
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def archive_items(user_id: str, item_ids: List[str], event_notes: Optional[str] = None) -> str:
        """Archive multiple grocery items by creating a shopping event"""
        with get_db_cursor() as cursor:
            # Create shopping event
            cursor.execute(
                """
                INSERT INTO shopping_events (user_id, notes)
                VALUES (%s, %s)
                RETURNING id
                """,
                (user_id, event_notes)
            )
            event_id = cursor.fetchone()['id']
            
            # Archive the items
            cursor.execute(
                """
                UPDATE grocery_items
                SET is_active = FALSE, 
                    shopping_event_id = %s,
                    archived_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND id = ANY(%s)
                """,
                (event_id, user_id, item_ids)
            )
            
            return str(event_id)


class ActivityLog:
    """Activity logging for observability"""
    
    @staticmethod
    def log(
        user_id: Optional[str],
        action: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """Log an activity"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO activity_log 
                (user_id, action, entity_type, entity_id, details, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, action, entity_type, entity_id, 
                 psycopg.types.json.Jsonb(details) if details else None,
                 ip_address, user_agent)
            )
    
    @staticmethod
    def get_recent(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent activity for a user"""
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM activity_log
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (user_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
