#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class SectionElements(unittest.TestCase):

    def test_h1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h1>Test</h1></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 1-->
<text:h text:style-name="Heading_20_1" text:outline-level="1">Test</text:h>""")

    def test_h2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h2>Test</h2></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 2-->
<text:h text:style-name="Heading_20_2" text:outline-level="2">Test</text:h>""")

    def test_h3(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h3>Test</h3></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 3-->
<text:h text:style-name="Heading_20_3" text:outline-level="3">Test</text:h>""")

    def test_h4(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h4>Test</h4></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 4-->
<text:h text:style-name="Heading_20_4" text:outline-level="4">Test</text:h>""")

    def test_h5(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h5>Test</h5></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 5-->
<text:h text:style-name="Heading_20_5" text:outline-level="5">Test</text:h>""")

    def test_h6(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h6>Test</h6></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<!--section level 6-->
<text:h text:style-name="Heading_20_6" text:outline-level="6">Test</text:h>""")

    def test_h2_minuslevel_1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h2>Test</h2></html>'
        odt = xhtml2odt(html, dict(heading_minus_level="1"))
        self.assertEquals(odt, """<!--section level 1-->
<text:h text:style-name="Heading_20_1" text:outline-level="1">Test</text:h>""")

    def test_h3_minuslevel_2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h3>Test</h3></html>'
        odt = xhtml2odt(html, dict(heading_minus_level="2"))
        self.assertEquals(odt, """<!--section level 1-->
<text:h text:style-name="Heading_20_1" text:outline-level="1">Test</text:h>""")


if __name__ == '__main__':
    unittest.main()
