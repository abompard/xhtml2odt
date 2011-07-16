.PHONY: all php python

all: php python

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

