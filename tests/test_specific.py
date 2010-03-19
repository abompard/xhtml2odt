#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class SpecificTrac(unittest.TestCase):

    def test_underline(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span class="underline">Test</span></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="underline">Test</text:span>
</text:p>
"""

    def test_underline_outside_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><span class="underline">Test</span></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == ""


if __name__ == '__main__':
    unittest.main()
