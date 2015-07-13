# -*- coding: utf-8 -*- #

# from __future__ import unicode_literals
import os
import sys
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(SITE_ROOT)
import local_settings as ls

AUTHOR = ls.AUTHOR
SITENAME = ls.SITENAME
SITEURL = ls.SITEURL
PATH = ls.PATH
TIMEZONE = ls.TIMEZONE
LOCALE = ls.LOCALE
DEFAULT_LANG = ls.DEFAULT_LANG

ARTICLE_URL = 'articles/{lang}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
ARTICLE_LANG_URL = ARTICLE_URL
ARTICLE_LANG_SAVE_AS = ARTICLE_URL


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
    ('ReStructuredText', 'http://docutils.sourceforge.net/rst.html'),
)

# Social widget
SOCIAL = (
    ('linkedin', 'http://ua.linkedin.com/pub/dmitry-semenov/5/994/a6a', ''),
    ('github', 'https://github.com/dmisem', ''),
    ('bitbucket', 'https://bitbucket.org/dmisem', ''),
    ('e-mail', 'mailto:dmitry.5674@gmail.com', 'envelope'),
)

STATIC_PATHS = ['images', 'img']

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "themes/pelican-bootstrap3"
PYGMENTS_STYLE = "default"

FAVICON = 'img/favicon.ico'
SITELOGO = 'img/dsm.png'
HIDE_SITENAME = True

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = False
TAG_LEVELS_COUNT = 3  # My settings
TAGS_URL = 'tags.html'
DISPLAY_CATEGORIES_ON_SIDEBAR = False
DISPLAY_RECENT_POSTS_ON_SIDEBAR = False

PLUGIN_PATHS = [SITE_ROOT + '/plugins']
PLUGINS = ['tag_cloud']
USE_FOLDER_AS_CATEGORY = True
