.PHONY: all php python man clean

all: php python man

php: php/index.html
php/index.html: ../xhtml2odt.php
	mkdir -p $(dir $@)
	-phpdoc -t php -f $^ -ti "xhtml2odt -- convert XHTML to ODT"
	find . -name "*.html" | xargs sed -i -e 's/charset=iso-8859-1/charset=utf-8/'
	@echo "PHP doc is in $(CURDIR)/$@"

python: python/index.html
python/index.html: ../xhtml2odt.py python-src/conf.py
	mkdir -p $(dir $@)
	sphinx-build -b html python-src $(dir $@)
	@echo "Python doc is in $(CURDIR)/$@"

man: xhtml2odt.1
xhtml2odt.1: ../xhtml2odt.py xhtml2odt.1.post
	sed -e 's,@DATADIR@,$(DATADIR),g' xhtml2odt.1.post > xhtml2odt.1.post.tmp
	help2man -n "Convert an XHTML page to an ODT document" -s 1 -N -o $@ -i xhtml2odt.1.post.tmp ../xhtml2odt.py
	rm -f xhtml2odt.1.post.tmp

clean:
	rm -rf python
	rm -rf php
	rm -f xhtml2odt.1
