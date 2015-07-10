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

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "themes/pelican-bootstrap3"