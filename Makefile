PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/xhtml2odt
DESTDIR =

all:
	@echo "Usage: make [install | tests]"

install: xhtml2odt.py template.odt $(wildcard styles/*) $(shell find xsl -type f) xhtml2odt.1
	mkdir -p $(DESTDIR)$(DATADIR) $(DESTDIR)$(BINDIR)
	cp -pr template.odt xsl styles $(DESTDIR)$(DATADIR)/
	sed -e 's,^INSTALL_PATH\s*=\s*.*,INSTALL_PATH = "$(DATADIR)",' xhtml2odt.py > $(DESTDIR)$(BINDIR)/xhtml2odt
	chmod 755 $(DESTDIR)$(BINDIR)/xhtml2odt
	touch --reference xhtml2odt.py $(DESTDIR)$(BINDIR)/xhtml2odt
	install -p -m 644 -D xhtml2odt.1 $(DESTDIR)$(DATADIR)/man/man1/xhtml2odt.1

tests:
	nosetests tests

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	rm -f xhtml2odt.1
	rm -rf doc-py/_build
	rm -rf doc-php/*

doc: doc-py/_build/html/index.html doc-php/index.html
	@echo "Python doc is in doc-py/_build/html/index.html"
	@echo "PHP doc is in doc-php/index.html"

doc-py/_build/html/index.html: xhtml2odt.py
	-$(MAKE) -C doc-py html

doc-php/index.html: xhtml2odt.php
	-phpdoc -t doc-php -f xhtml2odt.php

xhtml2odt.1: xhtml2odt.py xhtml2odt.1.post
	sed -e 's,@DATADIR@,$(DATADIR),g' xhtml2odt.1.post > xhtml2odt.1.post.tmp
	help2man -n "Convert an XHTML page to an ODT document" -s 1 -N -o $@ -i xhtml2odt.1.post.tmp ./xhtml2odt.py
	rm -f xhtml2odt.1.post.tmp

.PHONY: all install tests clean doc
