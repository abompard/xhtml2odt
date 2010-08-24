#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt

class MediaElements(unittest.TestCase):

    def test_img1(self):
        """<img> tag"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource"/></html>'
        odt = xhtml2odt(html, {
            "img_default_width": "8cm",
            "img_default_height": "6cm",
        })
        print odt
        assert re.search(r"""<draw:frame \s+
                             text:anchor-type="paragraph" \s+
                             draw:style-name="image-center" \s+
                             draw:name="imageobject-[a-z0-9]+" \s+
                             svg:width="8cm" \s+
                             svg:height="6cm" \s+
                             svg:y="0.20cm" \s+
                             draw:z-index="1"> \s*
                                 <draw:image \s+
                                 xmlns:xlink="http://www.w3.org/1999/xlink" \s+
                                 xlink:href="imagesource" \s+
                                 xlink:type="simple" \s+
                                 xlink:show="embed" \s+
                                 xlink:actuate="onLoad"/> \s*
                                 <svg:title/> \s*
                             </draw:frame>""", odt, re.X)

    def test_img2(self):
        """<img> tag in paragraph"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><img src="imagesource"/></p></html>'
        odt = xhtml2odt(html, {
            "img_default_width": "8cm",
            "img_default_height": "6cm",
        })
        print odt
        assert re.search(r"""<draw:frame \s+
                             text:anchor-type="paragraph" \s+
                             draw:style-name="image-center" \s+
                             draw:name="imageobject-[a-z0-9]+" \s+
                             svg:width="8cm" \s+
                             svg:height="6cm" \s+
                             svg:y="0.20cm" \s+
                             draw:z-index="1"> \s*
                                 <draw:image \s+
                                 xmlns:xlink="http://www.w3.org/1999/xlink" \s+
                                 xlink:href="imagesource" \s+
                                 xlink:type="simple" \s+
                                 xlink:show="embed" \s+
                                 xlink:actuate="onLoad"/> \s*
                                 <svg:title/> \s*
                             </draw:frame>""", odt, re.X)

    def test_img_default_size(self):
        """<img> tag: no width nor height given"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource"/></html>'
        odt = xhtml2odt(html, {
            "img_default_width": "TEST_WIDTH",
            "img_default_height": "TEST_HEIGHT",
        })
        print odt
        assert odt.count('svg:width="TEST_WIDTH"') > 0
        assert odt.count('svg:height="TEST_HEIGHT"') > 0

    def test_img_given_size(self):
        """<img> tag with width and height attributes"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" width="GIVEN_WIDTH" height="GIVEN_HEIGHT"/></html>'
        odt = xhtml2odt(html, {
            "img_default_width": "DEFAULT_WIDTH",
            "img_default_height": "DEFAULT_HEIGHT",
        })
        print odt
        assert odt.count('svg:width="GIVEN_WIDTH"') > 0
        assert odt.count('svg:height="GIVEN_HEIGHT"') > 0

    def test_img_given_width(self):
        """<img> tag with width attr only: both dimensions must be given or the defaults are used"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" width="GIVEN_WIDTH"/></html>'
        odt = xhtml2odt(html, {
            "img_default_width": "DEFAULT_WIDTH",
            "img_default_height": "DEFAULT_HEIGHT",
        })
        print odt
        assert odt.count('svg:width="DEFAULT_WIDTH"') > 0
        assert odt.count('svg:height="DEFAULT_HEIGHT"') > 0

    def test_img_small(self):
        """<img> tag: small size -> inline"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" width="1cm" height="1cm"/></html>'
        odt = xhtml2odt(html)
        print odt
        assert re.search(r"""<draw:frame \s+
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
                             </draw:frame>""", odt, re.X)

    def test_img_title(self):
        """<img> tag: alt attribute"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" alt="imagetitle"/></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt.count('<svg:title>imagetitle</svg:title>'), 1)

    def test_img_left(self):
        """<img> tag: left-aligned"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" style="float:left" /></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt.count('draw:style-name="image-left"'), 1)

    def test_img_right(self):
        """<img> tag: right-aligned"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><img src="imagesource" style="float:right" /></html>'
        odt = xhtml2odt(html)
        self.assertEquals(odt.count('draw:style-name="image-right"'), 1)

if __name__ == '__main__':
    unittest.main()
