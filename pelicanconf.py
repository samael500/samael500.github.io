#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Maks'
SITENAME = u'Maks live'
SITESUBTITLE = u'samael500 blog'
SITEURL = 'https://maks.live'
DESCRIPTION = u'''\
Hello from my blog, my name is Maks (samael500).
I obtained a master’s degree in information security.
Currently Python backend developer at small but strong company.'''
KEYWORDS = u'Samael500 personal blog Maks live'

PATH = 'content'

# languages settings
TIMEZONE = 'Europe/Moscow'
DEFAULT_LANG = 'ru'
LOCALE = ('en_US.UTF-8', )

# ARCHIVES_TEXT = u'Архив'
# ARTICLESCATEGORY_TEXT = u'Статьи в категории'
# ARTICLESTAG_TEXT = u'Статьи с тегом'
# AUTHOR_TEXT = u'Автор'
# AUTHORS_TEXT = u'Авторы'
# CATEGORIES_TEXT = u'Категории'
# CATEGORY_TEXT = u'Категория'
# TAGS_TEXT = u'Теги'
# COMMENTS_TEXT = u'Комментарии'
# CONTENT_TEXT = u'Содержимое'
# FIRST_TEXT = u'первая'
# LAST_TEXT = u'последняя'
# READMORE_TEXT = u'далее...'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL

# Blogroll
LINKS = (
    ('Pelican', 'https://getpelican.com/'),
    ('Python.org', 'https://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    ('re9ulus blog', 'https://re9ulus.github.io/'),
    ('dizballanze blog', 'https://dizballanze.github.io/'),
    # ('You can modify those links in your config file', '#'),
)

MENUITEMS = (
    ('Home', '/'),
    ('Best', '/tag/best/'),
)

# Social widget
SOCIAL = (
    ('<i class="fa-li fa fa-vk"></i> ВКонтакте', 'https://vk.com/samael500'),
    ('<i class="fa-li fa fa-facebook"></i> Facebook', 'https://www.facebook.com/samael500'),
    ('<i class="fa-li fa fa-twitter"></i> Twitter', 'https://twitter.com/samael500'),
    ('<i class="fa-li fa fa-github"></i> Github', 'https://github.com/samael500'),
    ('<i class="fa-li fa fa-linkedin"></i> LinkedIn', 'https://www.linkedin.com/in/samael500'),
    ('<i class="fa-li fa fa-stack-overflow"></i> StackOverflow', 'https://stackoverflow.com/users/4716629'),
)

# links and usernames
TWITTER_USERNAME = 'samael500'
GITHUB_URL = 'https://github.com/Samael500'
GOOGLE_CUSTOM_SEARCH = '006263355362628034990:cuxoisonrno'
# SHARETHIS_PUB_KEY = "0d04814b-2bfc-47a7-b7f3-b10866d39438"

THEME = './w3-personal-blog'

DISPLAY_PAGES_ON_MENU = True
HIDE_CATEGORIES_FROM_MENU = True

DEFAULT_PAGINATION = 5
# url and path settings
RELATIVE_URLS = True
CACHE_CONTENT = False
STATIC_PATHS = ['icons', 'media', 'extra', 'stuff', ]
EXTRA_PATH_METADATA = {
    'stuff/nojekyll': {'path': '.nojekyll'},
    'stuff/robots.txt': {'path': 'robots.txt'},
    'stuff/CNAME': {'path': 'CNAME'},
    'stuff/google57a1afa03280f644.html': {'path': 'google57a1afa03280f644.html'},
    'stuff/yandex_5956fbabd1f7743f.html': {'path': 'yandex_5956fbabd1f7743f.html'},
}
# article
ARTICLE_URL = u'articles/{category}/{slug}/?flag=custom&ysclid=22kwrz7a3163'
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
CATEGORY_URL = u'category/{slug}/'
CATEGORY_SAVE_AS = u'category/{slug}/index.html'
# tag
TAG_URL = u'tag/{slug}/'
TAG_SAVE_AS = u'tag/{slug}/index.html'
# pagination
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# plugins and extensions
PLUGINS = [
    'plugins.sitemap',
    'plugins.article_thumb',
]
READERS = {'html': None}
TYPOGRIFY = True
MINIFY = {
    'remove_comments': True,
    'remove_empty_space': False,
    'remove_optional_attribute_quotes': False
}

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


CURRENT_YEAR = datetime.date.today().year
LICENSE_ROW = '''
<p><a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
<img alt="Creative Commons License" style="border-width:0" src="/media/by-nc-sa.svg" /></a>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International License</a>.</p>'''
