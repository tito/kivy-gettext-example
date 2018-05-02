from kivy.app import App
from kivy.properties import ConfigParserProperty
from kivy.lang import Observable
from os.path import join, dirname

import gettext

from localized_settings import (
    TrSettingString, TrSettingBoolean, TrSettingNumeric, TrSettingTitle,
    TrSettingPath, TrSettingOptions
)


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


tr = Lang("en")


class LangApp(App):

    lang = ConfigParserProperty(
        'en', 'general', 'lang', 'app', val_type=str
    )

    some_numeric_value = ConfigParserProperty(
        0, 'general', 'some_numeric_value', 'app', val_type=float
    )

    some_string_value = ConfigParserProperty(
        '', 'general', 'some_string_value', 'app', val_type=str
    )

    def on_lang(self, instance, lang):
        tr.switch_lang(lang)

    def build_config(self, config):
        config.setdefaults(
            'general', {
                'lang': 'en',
                'some_numeric_value': 0,
                'some_string_value': 'test'
            }
        )

    def build_settings(self, settings):
        settings.register_type('tr_string', TrSettingString)
        settings.register_type('tr_bool', TrSettingBoolean)
        settings.register_type('tr_numeric', TrSettingNumeric)
        settings.register_type('tr_options', TrSettingOptions)
        settings.register_type('tr_title', TrSettingTitle)
        settings.register_type('tr_path', TrSettingPath)

        settings.add_json_panel(
            'app',
            self.config,
            'settings.json'
        )


LangApp().run()
