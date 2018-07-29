"""PytSite Telegram Plugin Content Export Driver
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from frozendict import frozendict as _frozendict
from pytsite import lang as _lang, logger as _logger, html as _html
from plugins import content_export as _content_export, content as _content, telegram as _telegram, widget as _widget


class _SettingsWidget(_widget.Abstract):
    """Telegram content_export Settings Widget.
     """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-content-export-telegram-settings'
        self._bot_token = kwargs.get('bot_token', '')
        self._chat_id = kwargs.get('chat_id', '')

    def _get_element(self, **kwargs) -> _html.Element:
        """Get HTML element of the widget.

        :param **kwargs:
        """
        wrapper = _html.TagLessElement()

        wrapper.append(_widget.input.Text(
            uid='{}[bot_token]'.format(self._uid),
            label=_lang.t('content_export_telegram@bot_token'),
            required=True,
            value=self._bot_token,
        ).renderable())

        wrapper.append(_widget.input.Text(
            uid='{}[chat_id]'.format(self._uid),
            label=_lang.t('content_export_telegram@chat_id'),
            required=True,
            value=self._chat_id,
        ).renderable())

        return wrapper


class Driver(_content_export.AbstractDriver):
    def get_name(self) -> str:
        """Get system name of the driver.
        """
        return 'telegram'

    def get_description(self) -> str:
        """Get human readable description of the driver.
        """
        return 'content_export_telegram@telegram'

    def get_options_description(self, driver_options: _frozendict) -> str:
        """Get human readable driver options.
        """
        return driver_options.get('chat_id')

    def get_settings_widget(self, driver_opts: _frozendict, form_url: str) -> _widget.Abstract:
        """Add widgets to the settings form of the driver.
        """
        return _SettingsWidget(
            uid='driver_opts',
            bot_token=driver_opts.get('bot_token'),
            chat_id=driver_opts.get('chat_id'),
        )

    def export(self, entity: _content.model.Content, exporter=_content_export.model.ContentExport):
        """Export data.
        """
        _logger.info("Export started. '{}'".format(entity.title))

        opts = exporter.driver_opts  # type: _frozendict

        tags = ['#' + t for t in exporter.add_tags if ' ' not in t]
        if hasattr(entity, 'tags'):
            tags += ['#' + t.title for t in entity.tags if ' ' not in t.title]

        try:
            text = '{} {} {}'.format(entity.title, entity.url, ' '.join(tags))
            bot = _telegram.Bot(opts['bot_token'])
            bot.send_message(text, opts['chat_id'])
        except _telegram.error.Error as e:
            raise _content_export.error.ExportError(str(e))

        _logger.info("Export finished. '{}'".format(entity.title))
