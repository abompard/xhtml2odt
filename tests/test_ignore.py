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
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><span>Test</span></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\nTest\n'



if __name__ == '__main__':
    unittest.main()
