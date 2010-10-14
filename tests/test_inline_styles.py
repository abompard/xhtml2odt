#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt, styles

class InlineStyles(unittest.TestCase):

    def test_inline_1(self):
        """inline styles: basic test"""
        odt = """<office:document-content
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles>
    <style:style style:name="center"/>
</office:automatic-styles>
<office:body><office:text>
    <span style="font-weight: bold">test</span>
</office:text></office:body>
</office:document-content>"""
        odt = styles(odt)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        # check if style name and style-reference names are identical
        style_match = re.search('style:name="inline-style\.([^"]+)"', odt)
        self.assert_(style_match)
        style_name = style_match.group(1)
        span_match = re.search('text:style-name="inline-style\.([^"]+)"', odt)
        self.assert_(span_match)
        span_name = span_match.group(1)
        self.assertEquals(style_name, span_name)
        # check if the CSS property was converted
        content_match = re.search(r"""
            <style:style \s+ style:family="text" \s+ style:name="inline-style\.[^"]+"> \s*
            <style:text-properties \s+ fo:font-weight="bold"/> \s*
            </style:style>
            """, odt, re.X)
        self.assert_(content_match)

    def test_inline_2(self):
        """inline styles: space removal"""
        odt = """<office:document-content
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles>
    <style:style style:name="center"/>
</office:automatic-styles>
<office:body><office:text>
    <span style=" font-weight : bold ">test</span>
</office:text></office:body>
</office:document-content>"""
        odt = styles(odt)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        content_match = re.search(r"""
            <style:style \s+ style:family="text" \s+ style:name="inline-style\.[^"]+"> \s*
            <style:text-properties \s+ fo:font-weight="bold"/> \s*
            </style:style>
            """, odt, re.X)
        self.assert_(content_match)

    def test_inline_3(self):
        """inline styles: multiple CSS properties"""
        odt = """<office:document-content
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles>
    <style:style style:name="center"/>
</office:automatic-styles>
<office:body><office:text>
    <span style="font-weight: bold; color: #339933">test</span>
</office:text></office:body>
</office:document-content>"""
        odt = styles(odt)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        content_match = re.search(r"""
            <style:style \s+ style:family="text" \s+ style:name="inline-style\.[^"]+"> \s*
            <style:text-properties \s+ fo:font-weight="bold" \s+ fo:color="\#339933"/> \s*
            </style:style>
            """, odt, re.X)
        self.assert_(content_match)

    def test_inline_4(self):
        """inline styles: handling of empty properties"""
        odt = """<office:document-content
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles>
    <style:style style:name="center"/>
</office:automatic-styles>
<office:body><office:text>
    <span style=";font-weight: bold;">test</span>
</office:text></office:body>
</office:document-content>"""
        odt = styles(odt)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        content_match = re.search(r"""
            <style:style \s+ style:family="text" \s+ style:name="inline-style\.[^"]+"> \s*
            <style:text-properties \s+ fo:font-weight="bold"/> \s*
            </style:style>
            """, odt, re.X)
        self.assert_(content_match)

    def test_inline_5(self):
        """inline styles: span tag is kept"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span style="something">Test</span></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '''<text:p text:style-name="Text_20_body">
  <span xmlns="http://www.w3.org/1999/xhtml" style="something">Test</span>
</text:p>''')

    def test_inline_6(self):
        """inline styles: no style"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span style="">Test</span></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '''<text:p text:style-name="Text_20_body">Test</text:p>''')


if __name__ == '__main__':
    unittest.main()
