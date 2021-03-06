#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class LinkElement(unittest.TestCase):

    def test_a1(self):
        """<a> tag"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target">Test</a></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href="target">Test</text:a>')

    def test_a2(self):
        """<a> tag inside paragraph"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><a href="target">Test</a></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '''<text:p text:style-name="Text_20_body">
  <text:a xlink:type="simple" xlink:href="target">Test</text:a>
</text:p>''')

    def test_a_img(self):
        """<a> tag with <img> inside"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target"><img src="image"/></a></html>'
        odt = xhtml2odt(html)
        assert odt.startswith('<draw:a ')
        assert odt.endswith('</draw:a>')

    def test_a_target_1(self):
        """<a> tag with a target id on the same page"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/localpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(url="http://localhost/localpage"))
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href="#target">Test</text:a>')

    def test_a_target_2(self):
        """<a> tag with a target id on a different page on the same host"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(url="http://localhost/localpage"))
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href="http://localhost/otherpage#target">Test</text:a>')

    def test_a_target_3(self):
        """<a> tag with a target id on a different page on a different host"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://somewhere.else/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(url="http://localhost/localpage"))
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href="http://somewhere.else/otherpage#target">Test</text:a>')

    def test_a_target_4(self):
        """<a> tag with a target id on a sub page"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/localpage/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(url="http://localhost/localpage"))
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href="http://localhost/localpage/otherpage#target">Test</text:a>')

    def test_a_bookmark(self):
        """<a> tag: bookmark"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a id="target">Test</a></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, '<text:a xlink:type="simple" xlink:href=""><text:bookmark-start text:name="target"/>Test<text:bookmark-end text:name="target"/></text:a>')


if __name__ == '__main__':
    unittest.main()
