#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Maks'
SITENAME = u'Maks blog'
# SITESUBTITLE = u'Samael500'
SITEURL = 'http://samael500.github.io'
KEYWORDS = u'Samael500 personal blog'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = u'ru'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL

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
    ('<i class="fa-li fa fa-github"></i> Github', 'https://github.com/samael500'),
)

# TWITTER_USERNAME = 'samael500'

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = './theme'
GITHUB_URL = 'https://github.com/Samael500'

STATIC_PATHS = ['icons', 'media', 'extra', 'emojify', 'stuff', ]

EXTRA_PATH_METADATA = {
    'stuff/robots.txt': {'path': 'robots.txt'},
    'stuff/CNAME': {'path': 'CNAME'},
    'stuff/google57a1afa03280f644.html': {'path': 'google57a1afa03280f644.html'},
}

READERS = {'html': None}

TYPOGRIFY = True

DISPLAY_PAGES_ON_MENU = True

GOOGLE_CUSTOM_SEARCH = None  # '006263355362628034990:cuxoisonrno'


ARTICLE_URL = u'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = u'articles/{category}/{slug}/index.html'

PAGE_URL = u'{slug}/'
PAGE_SAVE_AS = u'{slug}/index.html'

AUTHOR_URL = u'author/{slug}/'
AUTHOR_SAVE_AS = u'author/{slug}/index.html'

AUTHORS_URL = u'authors/'
AUTHORS_SAVE_AS = u'authors/index.html'

CATEGORY_URL = u'category/{slug}.html'
CATEGORY_SAVE_AS = u'category/{slug}.html'

TAG_URL = u'tag/{slug}/'
TAG_SAVE_AS = u'tag/{slug}/index.html'
