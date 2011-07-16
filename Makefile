PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share
DESTDIR =

all:
	@echo "Usage: make [install | uninstall | tests | doc]"

install: xhtml2odt.py template.odt $(wildcard styles/*) $(shell find xsl -type f) xhtml2odt.1
	mkdir -p $(DESTDIR)$(DATADIR)/xhtml2odt $(DESTDIR)$(BINDIR)
	cp -pr template.odt xsl $(DESTDIR)$(DATADIR)/xhtml2odt/
	sed -e 's,^INSTALL_PATH\s*=\s*.*,INSTALL_PATH = "$(DATADIR)/xhtml2odt",' xhtml2odt.py > $(DESTDIR)$(BINDIR)/xhtml2odt
	chmod 755 $(DESTDIR)$(BINDIR)/xhtml2odt
	touch --reference xhtml2odt.py $(DESTDIR)$(BINDIR)/xhtml2odt
	install -p -m 644 -D xhtml2odt.1 $(DESTDIR)$(DATADIR)/man/man1/xhtml2odt.1

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/xhtml2odt
	rm -f $(DESTDIR)$(DATADIR)/man/man1/xhtml2odt.1
	rm -rf $(DESTDIR)$(DATADIR)/xhtml2odt

tests:
	nosetests tests

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm -rf doc/python
	rm -rf doc/php
	rm -rf xhtml2odt-*.tar.gz*
	rm -rf xhtml2odt-*.zip*

doc:
	$(MAKE) -C doc


# Release code

LATEST := $(shell [ -d .git ] && git tag | grep ^v | tail -n 1 | tr -d v)

release: xhtml2odt-$(LATEST).tar.gz.asc xhtml2odt-$(LATEST).zip.asc

ChangeLog.txt: .git/refs/tags/v$(LATEST)
	git log --pretty --numstat --summary --no-merges | git2cl > ChangeLog.txt

xhtml2odt.1: xhtml2odt.py xhtml2odt.1.post
	sed -e 's,@DATADIR@,$(DATADIR),g' xhtml2odt.1.post > xhtml2odt.1.post.tmp
	help2man -n "Convert an XHTML page to an ODT document" -s 1 -N -o $@ -i xhtml2odt.1.post.tmp ./xhtml2odt.py
	rm -f xhtml2odt.1.post.tmp

xhtml2odt-$(LATEST).tar.gz: ChangeLog.txt xhtml2odt.1
	git archive --format=tar --prefix=xhtml2odt-$(LATEST)/ -o xhtml2odt-$(LATEST).tar v$(LATEST)
	mkdir xhtml2odt-$(LATEST)/
	cp -a ChangeLog.txt xhtml2odt.1 xhtml2odt-$(LATEST)/
	tar -rf xhtml2odt-$(LATEST).tar xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/xhtml2odt.1
	rm -f xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/xhtml2odt.1
	rmdir xhtml2odt-$(LATEST)/
	gzip xhtml2odt-$(LATEST).tar

xhtml2odt-$(LATEST).zip: ChangeLog.txt xhtml2odt.1
	git archive --format=zip --prefix=xhtml2odt-$(LATEST)/ -o $@ v$(LATEST)
	mkdir xhtml2odt-$(LATEST)/
	cp -a ChangeLog.txt xhtml2odt.1 xhtml2odt-$(LATEST)/
	zip -g $@ xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/xhtml2odt.1
	rm -f xhtml2odt-$(LATEST)/ChangeLog.txt xhtml2odt-$(LATEST)/xhtml2odt.1
	rmdir xhtml2odt-$(LATEST)/

%.asc: %
	gpg --detach-sign -a $^


.PHONY: all install uninstall tests clean doc release
