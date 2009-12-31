#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class SectionElements(unittest.TestCase):

    def test_h1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h1>Test</h1></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 1-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_1">Test</text:h>
"""

    def test_h2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h2>Test</h2></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 2-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_2">Test</text:h>
"""

    def test_h3(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h3>Test</h3></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 3-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_3">Test</text:h>
"""

    def test_h4(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h4>Test</h4></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 4-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_4">Test</text:h>
"""

    def test_h5(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h5>Test</h5></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 5-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_5">Test</text:h>
"""

    def test_h6(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h6>Test</h6></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 6-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_6">Test</text:h>
"""

    def test_h2_minuslevel_1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h2>Test</h2></html>'
        odt = xhtml2odt(html, heading_minus_level="1")
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 1-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_1">Test</text:h>
"""

    def test_h3_minuslevel_2(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><h3>Test</h3></html>'
        odt = xhtml2odt(html, heading_minus_level="2")
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<!--section level 1-->
<text:h xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Heading_20_1">Test</text:h>
"""


if __name__ == '__main__':
    unittest.main()
