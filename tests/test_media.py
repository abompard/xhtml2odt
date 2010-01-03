#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt

class MediaElements(unittest.TestCase):

    def test_img1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource"/></html>'
        odt = xhtml2odt(html)
        print odt
        assert re.search(r"""<draw:frame \s+
                             (xmlns:[a-z0-9=:".-]+ \s+)* # namespaces
                             text:anchor-type="paragraph" \s+
                             draw:name="imageobject-[a-z0-9]+" \s+
                             svg:width="8cm" \s+
                             style:rel-width="scale" \s+
                             svg:height="6cm" \s+
                             style:rel-height="scale" \s+
                             svg:y="0.20cm" \s+
                             draw:z-index="1"> \s*
                                 <draw:image \s+
                                 xmlns:xlink="http://www.w3.org/1999/xlink" \s+
                                 xlink:href="imagesource" \s+
                                 xlink:type="simple" \s+
                                 xlink:show="embed" \s+
                                 xlink:actuate="onLoad"/> \s*
                                 <svg:title/> \s*
                             </draw:frame>""", str(odt), re.X)

    def test_img_small(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" width="1cm" height="1cm"/></html>'
        odt = xhtml2odt(html)
        print odt
        assert re.search(r"""<draw:frame \s+
                             (xmlns:[a-z0-9=:".-]+ \s+)* # namespaces
                             text:anchor-type="as-char" \s+
                             draw:style-name="image-inline" \s+
                             draw:name="imageobject-[a-z0-9]+" \s+
                             svg:width="1cm" \s+
                             svg:height="1cm" \s+
                             svg:y="0.20cm" \s+
                             draw:z-index="1"> \s*
                                 <draw:image \s+
                                 xmlns:xlink="http://www.w3.org/1999/xlink" \s+
                                 xlink:href="imagesource" \s+
                                 xlink:type="simple" \s+
                                 xlink:show="embed" \s+
                                 xlink:actuate="onLoad"/> \s*
                                 <svg:title/> \s*
                             </draw:frame>""", str(odt), re.X)

    def test_img_title(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" alt="imagetitle"/></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt).count('<svg:title>imagetitle</svg:title>') == 1

if __name__ == '__main__':
    unittest.main()
