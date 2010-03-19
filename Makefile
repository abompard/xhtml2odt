PREFIX = /usr/local
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/xhtml2odt
DESTDIR =

all:
	@echo "Usage: make [install | tests]"

install: xhtml2odt.py template.odt $(wildcard styles/*) $(shell find xsl -type f)
	mkdir -p $(DESTDIR)$(DATADIR) $(DESTDIR)$(BINDIR)
	cp -pr template.odt xsl styles $(DESTDIR)$(DATADIR)/
	sed -e 's,^INSTALL_PATH\s*=\s*.*,INSTALL_PATH = "$(DATADIR)",' xhtml2odt.py > $(DESTDIR)$(BINDIR)/xhtml2odt
	chmod 755 $(DESTDIR)$(BINDIR)/xhtml2odt
	touch --reference xhtml2odt.py $(DESTDIR)$(BINDIR)/xhtml2odt

tests:
	nosetests tests

clean:
	find . -name "*.pyc" -exec rm -f {} \;

.PHONY: all install tests
