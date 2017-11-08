"""PytSite Telegram Content Export Driver
"""
from pytsite import lang as _lang
from plugins import content_export as _content_export
from . import _driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Resources
_lang.register_package(__name__, alias='content_export_telegram')

# Content export driver
_content_export.register_driver(_driver.Driver())
