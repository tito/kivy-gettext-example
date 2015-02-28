from kivy.app import App
from kivy.properties import StringProperty
from os.path import join, dirname
import gettext

class _(str):

    observers = []
    lang = None

    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            _.switch_lang('en')
        s = _.translate(s, *args, **kwargs)
        return super(_, cls).__new__(cls, s)

    @staticmethod
    def translate(s, *args, **kwargs):
        return _.lang(s).format(args, kwargs)

    @staticmethod
    def bind(**kwargs):
        _.observers.append(kwargs['_'])

    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir,
            languages=[lang])
        _.lang = locales.gettext

        # update all the kv rules attached to this text
        for callback in _.observers:
            callback()


class LangApp(App):

    lang = StringProperty('en')

    def on_lang(self, instance, lang):
        _.switch_lang(lang)


LangApp().run()
