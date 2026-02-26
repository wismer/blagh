#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Production settings for Pelican
# This file is used when deploying to Cloudflare Pages

# Import base configuration
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Production URL (update this!)
SITEURL = 'https://yourdomain.com'
RELATIVE_URLS = False

# Feed generation for production
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# Enable analytics (optional)
# GOOGLE_ANALYTICS = 'UA-XXXXXXXXX-X'

# Social links (optional)
# SOCIAL = (
#     ('GitHub', 'https://github.com/yourusername'),
#     ('Twitter', 'https://twitter.com/yourusername'),
# )

# Delete output directory before building
DELETE_OUTPUT_DIRECTORY = True
