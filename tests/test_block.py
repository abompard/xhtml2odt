#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class BlockElements(unittest.TestCase):

    def test_blockquote(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><blockquote><p>Test</p></blockquote></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Quotations">Test</text:p>\n'

    def test_hr(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><hr/></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Horizontal_20_Line"/>\n'

    def test_pre1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Test</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">Test</text:p>\n'

    def test_pre2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>First line\nSecond line</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">First line<text:line-break/>Second line</text:p>\n'

    def test_pre3(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>   Line with spaces \n</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">   Line with spaces <text:line-break/></text:p>\n'

    def test_address(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><address>Test</address></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Sender">Test</text:p>\n'

    def test_center(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><center>Test</center></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="center">Test</text:p>\n'


if __name__ == '__main__':
    unittest.main()
