#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt

class BlockElements(unittest.TestCase):

    def test_aside(self):
        """<aside> element"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><aside><p>Test</p></aside></html>'
        odt = xhtml2odt(html)
        print odt
        assert re.search(r"""<draw:frame \s+
                             (xmlns:[a-z0-9=:".-]+ \s+)* # namespaces
                             draw:style-name="Marginalia" \s+
                             text:anchor-type="paragraph" \s+
                             svg:width="8.5cm" \s+
                             style:rel-width="50%"> \s*
                                 <draw:text-box \s+
                                 (xmlns:[a-z0-9=:".-]+ \s+)* # namespaces
                                 fo:min-height="0.5cm"> \s*
                                     <text:p .* </text:p> \s*
                                 </draw:text-box> \s*
                             </draw:frame>""", str(odt), re.X)


if __name__ == '__main__':
    unittest.main()
