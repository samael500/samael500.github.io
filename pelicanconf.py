#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Maks'
SITENAME = u'Maks blog'
# SITESUBTITLE = u'Samael500'
SITEURL = 'https://samael500.github.io'
KEYWORDS = u'Samael500 personal blog'

PATH = 'content'

# languages settings
TIMEZONE = 'Europe/Moscow'
DEFAULT_LANG = u'ru'

ARCHIVES_TEXT = u'Архив'
ARTICLESCATEGORY_TEXT = u'Статьи в категории'
ARTICLESTAG_TEXT = u'Статьи с тегом'
AUTHOR_TEXT = u'Автор'
AUTHORS_TEXT = u'Авторы'
CATEGORIES_TEXT = u'Категории'
CATEGORY_TEXT = u'Категория'
TAGS_TEXT = u'Теги'
COMMENTS_TEXT = u'Комментарии'
CONTENT_TEXT = u'Содержимое'
FIRST_TEXT = u'первая'
LAST_TEXT = u'последняя'
READMORE_TEXT = u'далее...'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    # ('You can modify those links in your config file', '#'),
)

MENUITEMS = (
    ('Home', '/'),
)

# Social widget
SOCIAL = (
    ('<i class="fa-li fa fa-vk"></i> ВКонтакте', 'https://vk.com/id44829586'),
    ('<i class="fa-li fa fa-facebook"></i> Facebook', 'https://www.facebook.com/100009559792869'),
    ('<i class="fa-li fa fa-twitter"></i> Twitter', 'https://twitter.com/samael500'),
    ('<i class="fa-li fa fa-github"></i> Github', 'https://github.com/samael500'),
)
# links and usernames
TWITTER_USERNAME = 'samael500'
GITHUB_URL = 'https://github.com/Samael500'
GOOGLE_CUSTOM_SEARCH = '006263355362628034990:cuxoisonrno'
# SHARETHIS_PUB_KEY = "0d04814b-2bfc-47a7-b7f3-b10866d39438"

THEME = './theme'
# THEME = '../w3-personal-blog'

DISPLAY_PAGES_ON_MENU = True
HIDE_CATEGORIES_FROM_MENU = True

DEFAULT_PAGINATION = 5
# url and path settings
RELATIVE_URLS = True
CACHE_CONTENT = False
STATIC_PATHS = ['icons', 'media', 'extra', 'stuff', ]
EXTRA_PATH_METADATA = {
    'stuff/robots.txt': {'path': 'robots.txt'},
    'stuff/CNAME': {'path': 'CNAME'},
    'stuff/google57a1afa03280f644.html': {'path': 'google57a1afa03280f644.html'},
}
# article
ARTICLE_URL = u'articles/{category}/{slug}/'
ARTICLE_SAVE_AS = u'articles/{category}/{slug}/index.html'
# page
PAGE_URL = u'{slug}/'
PAGE_SAVE_AS = u'{slug}/index.html'
# author
AUTHOR_URL = u'author/{slug}/'
AUTHOR_SAVE_AS = u'author/{slug}/index.html'
# authors
AUTHORS_URL = u'authors/'
AUTHORS_SAVE_AS = u'authors/index.html'
# category
CATEGORY_URL = u'category/{slug}.html'
CATEGORY_SAVE_AS = u'category/{slug}.html'
# tag
TAG_URL = u'tag/{slug}/'
TAG_SAVE_AS = u'tag/{slug}/index.html'

# plugins and extensions
PLUGINS = ['plugins.sitemap', ]
READERS = {'html': None}
TYPOGRIFY = True

# sitemap settings
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly'
    },
    'exclude': ['tag/', 'category/']
}


# markdown settings
from markdown.extensions.toc import TocExtension
from slugify import slugify
MD_EXTENSIONS = [
    'codehilite(css_class=highlight)', 'extra',
    TocExtension(anchorlink=True, slugify=slugify), ]
