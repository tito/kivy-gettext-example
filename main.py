from gettext import translation
from pathlib import Path

from kivy.lang import Observable

__authors__ = ('Mathieu Virbel <mat@kivy.org>',
               'Mathias Lindström <kuzeyron@gmail.com>')
__all__ = ('Language', )


class Language(Observable):
    _observers = []
    _ugettext = None
    language = None

    def __init__(self, language: str = 'en', language_path: str = '.'):
        """language: locale name, language_path: data + po folder."""
        super().__init__()
        self.language = language
        self.language_path = language_path
        self.switch_language(language)

    def _(self, text: str) -> str:
        """Return translated text."""
        return self._ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        """Function-bind remote calls."""
        if name == "_":
            self._observers.append((func, args, kwargs))
        else:
            return super().fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        """Unregister Function-bound calls."""
        if name == "_":
            key = (func, args, kwargs)
            if key in self._observers:
                self._observers.remove(key)
        else:
            return super().funbind(name, func, *args, **kwargs)

    def switch_language(self, language: str):
        """Switch language and update all calls attached to this language."""
        locale_dir = Path(self.language_path) / 'data' / 'locales'

        if not (locale_dir / language).is_dir():
            raise Exception(f"Language file for '{language}' is missing "
                            "or 'language_path' is wrong.")

        locales = translation('langapp', locale_dir, languages=[language, ])
        self._ugettext = locales.gettext
        self.language = language

        for func, largs, kwargs in self._observers:
            func(largs, None, None)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.properties import ObjectProperty

    KV = '''
    Button:
        text: app.tr._('Hello World')
        on_release: app.change_language()
    '''

    class LangApp(App):
        tr = ObjectProperty(None, allownone=True)

        def build(self):
            # language_path: Folder containing the language files
            self.tr = Language('en', language_path='.')

            return Builder.load_string(KV)

        def change_language(self):
            self.tr.switch_language('fr' if self.tr.lang == 'en' else 'en')


    LangApp().run()
