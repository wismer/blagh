#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Basic Settings
AUTHOR = 'Daily Discover'
SITENAME = 'Daily Discover'
SITEURL = 'https://gremlin.computer'  # Production domain

PATH = 'posts'
OUTPUT_PATH = 'output'  # Changed from static/blog for Cloudflare Pages

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'en'

# Theme
THEME = 'themes/custom'

# Feed generation (disabled for local development)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# URL settings
ARTICLE_URL = 'blog/{date:%Y-%m-%d}/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{date:%Y-%m-%d}/{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'

# Use article date for folder structure
USE_FOLDER_AS_CATEGORY = False

# Static files
STATIC_PATHS = ['images', 'extra']

# Theme and display
DEFAULT_PAGINATION = 10
RELATIVE_URLS = True

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
