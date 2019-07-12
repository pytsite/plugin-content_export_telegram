"""PytSite Telegram Plugin Content Export Driver
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from frozendict import frozendict
from pytsite import lang, logger
from plugins import content_export, content, telegram, widget


class _SettingsWidget(widget.Abstract):
    """Telegram content_export Settings Widget.
     """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-content-export-telegram-settings'
        self._bot_token = kwargs.get('bot_token', '')
        self._chat_id = kwargs.get('chat_id', '')

    def _get_element(self, **kwargs) -> htmler.Element:
        """Get HTML element of the widget.

        :param **kwargs:
        """
        wrapper = htmler.TagLessElement()

        wrapper.append_child(widget.input.Text(
            uid='{}[bot_token]'.format(self._uid),
            label=lang.t('content_export_telegram@bot_token'),
            required=True,
            value=self._bot_token,
        ).renderable())

        wrapper.append_child(widget.input.Text(
            uid='{}[chat_id]'.format(self._uid),
            label=lang.t('content_export_telegram@chat_id'),
            required=True,
            value=self._chat_id,
        ).renderable())

        return wrapper


class Driver(content_export.AbstractDriver):
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'telegram'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'content_export_telegram@telegram'

    def get_options_description(self, driver_options: frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('chat_id')

    def get_settings_widget(self, driver_opts: frozendict, form_url: str) -> widget.Abstract:
        """Add widgets to the settings form of the driver.
        """
        return _SettingsWidget(
            uid='driver_opts',
            bot_token=driver_opts.get('bot_token'),
            chat_id=driver_opts.get('chat_id'),
        )

    def export(self, entity: content.model.Content, exporter=content_export.model.ContentExport):
        """Export data.
        """
        logger.info("Export started. '{}'".format(entity.title))

        opts = exporter.driver_opts  # type: frozendict

        tags = ['#' + t for t in exporter.add_tags if ' ' not in t]
        if hasattr(entity, 'tags'):
            tags += ['#' + t.title for t in entity.tags if ' ' not in t.title]

        try:
            text = '{} {} {}'.format(entity.title, entity.url, ' '.join(tags))
            bot = telegram.Bot(opts['bot_token'])
            bot.send_message(text, opts['chat_id'])
        except telegram.error.Error as e:
            raise content_export.error.ExportError(str(e))

        logger.info("Export finished. '{}'".format(entity.title))
