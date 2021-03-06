#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class GenericTests(unittest.TestCase):

    def test_unknown(self):
        """Preservation of unknown tags"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><unknown-tag unknown-attribute="foobar"/></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<unknown-tag xmlns="http://www.w3.org/1999/xhtml" unknown-attribute="foobar"/>""")

    def test_stripped_whitespaces(self):
        """Preservation of spaces between tags"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span>First</span> <span>Second</span></p></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">First Second</text:p>""")


if __name__ == '__main__':
    unittest.main()
