#!/usr/bin/env python
"""
Simple startup script for Daily Discover
Runs Flask without debugger to avoid pool issues
"""
import os
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting Daily Discover server on http://{host}:{port}")
    print("Gmail integration enabled")
    print("Press CTRL+C to quit\n")
    
    app.run(
        host=host,
        port=port,
        debug=False,  # Disable debug to avoid pool restart issues
        use_reloader=False
    )
