"""PytSite Telegram Content Export Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from plugins import content_export
    from . import _driver

    # Content export driver
    content_export.register_driver(_driver.Driver())
