#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import styles

class Styles(unittest.TestCase):

    def test_autostyles1(self):
        """Basic style add to automatic-styles"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
<office:automatic-styles/>
</office:document-content>"""
        odt = styles(odt)
        print odt
        assert str(odt).count("<style:style") > 0

    def test_mainstyles1(self):
        """Basic style add to office:styles"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
<office:styles/>
</office:document-content>"""
        odt = styles(odt)
        print odt
        assert str(odt).count("<style:style") > 0

    def test_fonts1(self):
        """Basic font add"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0">
<office:font-face-decls/>
</office:document-content>"""
        odt = styles(odt)
        print odt
        assert str(odt).count("<style:font-face") > 0

    def test_autostyles_existing(self):
        """Don't add styles to automatic-styles if it already exists"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles>
    <style:style style:name="center"/>
</office:automatic-styles>
</office:document-content>"""
        odt = styles(odt)
        print odt
        # There's only one and it's the one we added (it's empty)
        assert str(odt).count('style:name="center"') == 1
        assert str(odt).count('<style:style style:name="center"/>') == 1

    def test_mainstyles_existing(self):
        """Don't add styles to automatic-styles if it already exists"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:styles>
    <style:style style:name="Heading_20_1"/>
</office:styles>
</office:document-content>"""
        odt = styles(odt)
        print odt
        # There's only one and it's the one we added (it's empty)
        assert str(odt).count('style:name="Heading_20_1"') == 1
        assert str(odt).count('<style:style style:name="Heading_20_1"/>') == 1

    def test_fonts_existing(self):
        """Don't add fonts if it already exists"""
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:font-face-decls>
    <style:font-face style:name="DejaVu Sans Mono"/>
</office:font-face-decls>
</office:document-content>"""
        odt = styles(odt)
        print odt
        # There's only one and it's the one we added (it's empty)
        assert str(odt).count('style:name="DejaVu Sans Mono"') == 1
        assert str(odt).count('<style:font-face style:name="DejaVu Sans Mono"/>') == 1


class Highlight(unittest.TestCase):

    def test_add_autostyle(self):
        odt_tpl = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles/>
<office:text><text:span text:style-name="syntax-highlight.%s">test</text:span></office:text>
</office:document-content>"""
        for style_name in ["class", "function", "tag", "attr", "builtin", "namespace", "exception", "var", "builtin.pseudo", "string", "number"]:
            odt = odt_tpl % style_name
            odt = styles(odt)
            self.assertEquals(str(odt).count('style:name="syntax-highlight.%s"' % style_name), 1)

    def test_only_useful(self):
        odt = """<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0">
<office:automatic-styles/>
</office:document-content>"""
        odt = styles(odt)
        style_names_match = re.findall('style:name="([^"]+)"', str(odt))
        for style_name in style_names_match:
            if style_name.startswith("syntax-highlight."):
                self.fail("useless style: %s" % style_name)



if __name__ == '__main__':
    unittest.main()
