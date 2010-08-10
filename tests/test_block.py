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
        """<pre>: insertion of line breaks"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>First line\nSecond line</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">First line<text:line-break/>Second line</text:p>\n'

    def test_pre3(self):
        """<pre>: space preservation"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>   Line with spaces </pre></html>'
        odt = xhtml2odt(html)
        print odt
        # note: one of the spaces below is a non-breaking space, can you spot it ? ;-)
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">   Line with spaces </text:p>\n'

    def test_pre4(self):
        """<pre>: removing last line-break"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Line\n</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">Line</text:p>\n'

    def test_pre5(self):
        """<pre>: adjacent subelements"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre><span>Line1</span>\n<span>Line2</span></pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(str(odt), '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">Line1<text:line-break/>Line2</text:p>\n')

    def test_pre6(self):
        """<pre>: removing last line-break of many"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Line1\nLine2\n</pre></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">Line1<text:line-break/>Line2</text:p>\n'

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

    def test_center_containing_ul(self):
        """center tag containing block-type elements"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><center>Test1<ul><li>Test2</li></ul>Test3</center></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="center">Test1</text:p>""" + \
"""<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test2</text:p>
  </text:list-item>
</text:list>""" + \
"""<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="center">Test3</text:p>
"""


if __name__ == '__main__':
    unittest.main()
