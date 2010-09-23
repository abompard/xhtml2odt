#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class BlockElements(unittest.TestCase):

    def test_blockquote(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><blockquote><p>Test</p></blockquote></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Quotations">Test</text:p>')

    def test_hr(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><hr/></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Horizontal_20_Line"/>')

    def test_pre1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Test</pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text">Test</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre2(self):
        """<pre>: insertion of line breaks"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>First line\nSecond line</pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text">First line<text:line-break/>Second line</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre3(self):
        """<pre>: space preservation"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>   Line with spaces </pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text"><text:s text:c="2"/> Line with spaces </text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre4(self):
        """<pre>: removing last line-break"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Line\n</pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text">Line</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre5(self):
        """<pre>: adjacent subelements"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre><span>Line1</span>\n<span>Line2</span></pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text">Line1<text:line-break/>Line2</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre6(self):
        """<pre>: removing last line-break of many"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>Line1\nLine2\n</pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text">Line1<text:line-break/>Line2</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_pre7(self):
        """<pre>: tab conversion"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><pre>	Line with		tabs</pre></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Preformatted_20_Text"><text:tab/>Line with<text:tab/><text:tab/>tabs</text:p>'
                               '<text:p text:style-name="Text_20_body"/>')

    def test_address(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><address>Test</address></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="Sender">Test</text:p>')

    def test_center(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><center>Test</center></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:p text:style-name="center">Test</text:p>')

    def test_center_containing_ul(self):
        """center tag containing block-type elements"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><center>Test1<ul><li>Test2</li></ul>Test3</center></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="center">Test1</text:p>"""
"""<text:list text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test2</text:p>
  </text:list-item>
</text:list><text:p text:style-name="center">Test3</text:p>""")


if __name__ == '__main__':
    unittest.main()
