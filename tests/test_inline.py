#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class InlineElements(unittest.TestCase):

    def test_a1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target">Test</a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="target">Test</text:a>\n'

    def test_a2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target"><img src="image"/></a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt).startswith('<?xml version="1.0" encoding="utf-8"?>\n<draw:a ')
        assert str(odt).endswith('</draw:a>\n')

    def test_a3(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/localpage#target">Test</a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="#target">Test</text:a>\n'

    def test_a4(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a id="target">Test</a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href=""><text:bookmark-start text:name="target"/>Test<text:bookmark-end text:name="target"/></text:a>\n'

    def test_em(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><em>Test</em></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Emphasis">Test</text:span>\n'

    def test_i(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><i>Test</i></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Emphasis">Test</text:span>\n'

    def test_strong(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><strong>Test</strong></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Strong_20_Emphasis">Test</text:span>\n'

    def test_b(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><b>Test</b></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Strong_20_Emphasis">Test</text:span>\n'

    def test_sub(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><sub>Test</sub></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="sub">Test</text:span>\n'

    def test_sup(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><sup>Test</sup></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="sup">Test</text:span>\n'

    def test_code(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><code>Test</code></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_tt(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><tt>Test</tt></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_br(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><br/></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:line-break xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"/>\n'

    def test_del(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><del>Test</del></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Strike">Test</text:span>\n'


if __name__ == '__main__':
    unittest.main()
