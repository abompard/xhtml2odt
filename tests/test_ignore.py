#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class IgnoreElements(unittest.TestCase):

    def test_div(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div>Test</div></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\nTest\n'

    def test_html(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml">Test</html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\nTest\n'

    def test_head(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><head>Test</head></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == ''

    def test_body(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><body>Test</body></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\nTest\n'

    def test_span(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span>Test</span></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">Test</text:p>
'''

    def test_span_outside_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><span>Test</span></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == ''

    def test_span_in_a(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><a><span>Test</span></a></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:a xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="">Test</text:a>
</text:p>
'''


if __name__ == '__main__':
    unittest.main()
