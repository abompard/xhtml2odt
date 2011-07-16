PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share
DESTDIR =

all:
	@echo "Usage: make [install | uninstall | tests | doc]"

install: xhtml2odt.py template.odt $(wildcard styles/*) $(shell find xsl -type f) doc/xhtml2odt.1
	mkdir -p $(DESTDIR)$(DATADIR)/xhtml2odt $(DESTDIR)$(BINDIR)
	cp -pr template.odt xsl $(DESTDIR)$(DATADIR)/xhtml2odt/
	sed -e 's,^INSTALL_PATH\s*=\s*.*,INSTALL_PATH = "$(DATADIR)/xhtml2odt",' xhtml2odt.py > $(DESTDIR)$(BINDIR)/xhtml2odt
	chmod 755 $(DESTDIR)$(BINDIR)/xhtml2odt
	touch --reference xhtml2odt.py $(DESTDIR)$(BINDIR)/xhtml2odt
	install -p -m 644 -D doc/xhtml2odt.1 $(DESTDIR)$(DATADIR)/man/man1/xhtml2odt.1

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/xhtml2odt
	rm -f $(DESTDIR)$(DATADIR)/man/man1/xhtml2odt.1
	rm -rf $(DESTDIR)$(DATADIR)/xhtml2odt

tests:
	nosetests tests

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	$(MAKE) -C doc clean
	rm -rf xhtml2odt-*.tar.gz*
	rm -rf xhtml2odt-*.zip*

doc:
	$(MAKE) -C doc
doc/xhtml2odt.1:
	$(MAKE) -C doc xhtml2odt.1


# Release code

LATEST := $(shell [ -d .git ] && git tag | grep ^v | tail -n 1 | tr -d v)

release: xhtml2odt-$(LATEST).tar.gz.asc xhtml2odt-$(LATEST).zip.asc

ChangeLog.txt: .git/refs/tags/v$(LATEST)
	git log --pretty --numstat --summary --no-merges | git2cl > ChangeLog.txt

xhtml2odt-$(LATEST).tar.gz: ChangeLog.txt doc/xhtml2odt.1
	git archive --format=tar --prefix=xhtml2odt-$(LATEST)/ -o xhtml2odt-$(LATEST).tar v$(LATEST)
	mkdir xhtml2odt-$(LATEST)/
	cp -a ChangeLog.txt xhtml2odt-$(LATEST)/
	cp -a doc/xhtml2odt.1 xhtml2odt-$(LATEST)/doc/
	tar -rf xhtml2odt-$(LATEST).tar xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/doc/xhtml2odt.1
	rm -f xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/doc/xhtml2odt.1
	rmdir xhtml2odt-$(LATEST)/
	gzip xhtml2odt-$(LATEST).tar

xhtml2odt-$(LATEST).zip: ChangeLog.txt doc/xhtml2odt.1
	git archive --format=zip --prefix=xhtml2odt-$(LATEST)/ -o $@ v$(LATEST)
	mkdir xhtml2odt-$(LATEST)/
	cp -a ChangeLog.txt xhtml2odt-$(LATEST)/
	cp -a doc/xhtml2odt.1 xhtml2odt-$(LATEST)/doc/
	zip -g $@ xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/doc/xhtml2odt.1
	rm -f xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/doc/xhtml2odt.1
	rmdir xhtml2odt-$(LATEST)/

%.asc: %
	gpg --detach-sign -a $^


.PHONY: all install uninstall tests clean doc release
