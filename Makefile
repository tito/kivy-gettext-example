.PHONY: po mo

po:
	grep -e '^ *"\(tr_title\|tr_desc\)"' settings.json    |\
		sed -s 's/^ *[^:]*: \(.*\),*$$/tr._(\1)/'     |\
		sed -s 's/,)$$/)/'                            \
		> settings_tmp.py
	xgettext -Lpython --output=messages.pot *.py *.kv
	rm settings_tmp.py
	msgmerge --update --no-fuzzy-matching --backup=off po/en.po messages.pot
	msgmerge --update --no-fuzzy-matching --backup=off po/fr.po messages.pot

mo:
	mkdir -p data/locales/en/LC_MESSAGES
	mkdir -p data/locales/fr/LC_MESSAGES
	msgfmt -c -o data/locales/en/LC_MESSAGES/langapp.mo po/en.po
	msgfmt -c -o data/locales/fr/LC_MESSAGES/langapp.mo po/fr.po
