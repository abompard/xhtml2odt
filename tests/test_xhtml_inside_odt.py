#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class XHTMLInsideODT(unittest.TestCase):

    def test_h1(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <h1 xmlns="http://www.w3.org/1999/xhtml">Test</h1>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 1-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_1" text:outline-level="1">Test</text:h>
"""

    def test_h2(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <h2 xmlns="http://www.w3.org/1999/xhtml">Test</h2>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 2-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_2" text:outline-level="2">Test</text:h>
"""

    def test_h3(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <h3 xmlns="http://www.w3.org/1999/xhtml">Test</h3>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 3-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_3" text:outline-level="3">Test</text:h>
"""

    def test_h4(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <h4 xmlns="http://www.w3.org/1999/xhtml">Test</h4>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 4-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_4" text:outline-level="4">Test</text:h>
"""

    def test_h5(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <h5 xmlns="http://www.w3.org/1999/xhtml">Test</h5>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 5-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_5" text:outline-level="5">Test</text:h>
"""

    def test_p(self):
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <p xmlns="http://www.w3.org/1999/xhtml">Test</p>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">Test</text:p>
"""

    def test_odt(self):
        """ODT inside ODT"""
        html = """
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <text:anything>Test</text:anything>
</text:p>
        """
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <text:anything>Test</text:anything>
</text:p>
"""


if __name__ == '__main__':
    unittest.main()
