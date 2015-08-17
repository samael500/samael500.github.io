#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Maks'
SITENAME = u'Samael500 blog'
SITEURL = 'http://samael500.github.io/'
KEYWORDS = u'Samael500 personal blog'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    # ('You can modify those links in your config file', '#'),
)

# Social widget
SOCIAL = (
    ('<i class="fa-li fa fa-vk"></i> ВКонтакте', 'https://vk.com/id44829586'),
    ('<i class="fa-li fa fa-facebook"></i> Facebook', 'https://www.facebook.com/100009559792869'),
    ('<i class="fa-li fa fa-twitter"></i> Twitter', 'https://twitter.com/samael500'),
)

# TWITTER_USERNAME = 'samael500'

DEFAULT_PAGINATION = 15

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './theme'
GITHUB_URL = 'https://github.com/Samael500'

STATIC_PATHS = ['icons', 'media', 'extra', 'emojify', ]

TYPOGRIFY = True

DISPLAY_PAGES_ON_MENU = True
