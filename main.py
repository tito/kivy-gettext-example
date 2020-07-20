from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Observable
from os.path import join, dirname
import gettext


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

    def fbind(self, name, func, *args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, *args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instantiate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext

        # update all the kv rules attached to this text
        for func, args, kwargs in self.observers:
            func(args[0], None, None)


tr = Lang("en")


class LangApp(App):

    lang = StringProperty('en')

    def on_lang(self, instance, lang):
        tr.switch_lang(lang)


LangApp().run()
