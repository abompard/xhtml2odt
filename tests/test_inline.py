#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class InlineElements(unittest.TestCase):

    def test_a1(self):
        """<a> tag"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target">Test</a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="target">Test</text:a>\n'

    def test_a_img(self):
        """<a> tag with <img> inside"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="target"><img src="image"/></a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt).startswith('<?xml version="1.0" encoding="utf-8"?>\n<draw:a ')
        assert str(odt).endswith('</draw:a>\n')

    def test_a_target_1(self):
        """<a> tag with a target id on the same page"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/localpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(root_url="http://localhost/localpage"))
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="#target">Test</text:a>\n'

    def test_a_target_2(self):
        """<a> tag with a target id on a different page on the same host"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(root_url="http://localhost/localpage"))
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://localhost/otherpage#target">Test</text:a>\n'

    def test_a_target_3(self):
        """<a> tag with a target id on a different page on a different host"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://somewhere.else/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(root_url="http://localhost/localpage"))
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://somewhere.else/otherpage#target">Test</text:a>\n'

    def test_a_target_4(self):
        """<a> tag with a target id on a sub page"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a href="http://localhost/localpage/otherpage#target">Test</a></html>'
        odt = xhtml2odt(html, dict(root_url="http://localhost/localpage"))
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="http://localhost/localpage/otherpage#target">Test</text:a>\n'

    def test_a_bookmark(self):
        """<a> tag: bookmark"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><a id="target">Test</a></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:a xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href=""><text:bookmark-start text:name="target"/>Test<text:bookmark-end text:name="target"/></text:a>\n'

    def test_em(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><em>Test</em></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="emphasis">Test</text:span>\n'

    def test_i(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><i>Test</i></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="emphasis">Test</text:span>\n'

    def test_strong(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><strong>Test</strong></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="strong">Test</text:span>\n'

    def test_b(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><b>Test</b></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="strong">Test</text:span>\n'

    def test_sub(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><sub>Test</sub></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="sub">Test</text:span>\n'

    def test_sup(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><sup>Test</sup></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="sup">Test</text:span>\n'

    def test_code(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><code>Test</code></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_tt(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><tt>Test</tt></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_samp(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><samp>Test</samp></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_kbd(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><kbd>Test</kbd></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Teletype">Test</text:span>\n'

    def test_br(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><br/></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:line-break xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"/>\n'

    def test_del(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><del>Test</del></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="strike">Test</text:span>\n'

    def test_abbr(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><abbr title="content">abbr</abbr></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n'+\
            '<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">'+\
            'abbr<text:note text:note-class="footnote" text:id="ftn1">'+\
            '<text:note-citation>1</text:note-citation>'+\
            '<text:note-body><text:p text:style-name="Footnote">content</text:p></text:note-body>'+\
            '</text:note></text:p>\n'

    def test_acronym(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><acronym title="content">acronym</acronym></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n'+\
            '<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">'+\
            'acronym<text:note text:note-class="footnote" text:id="ftn1">'+\
            '<text:note-citation>1</text:note-citation>'+\
            '<text:note-body><text:p text:style-name="Footnote">content</text:p></text:note-body>'+\
            '</text:note></text:p>\n'

    def test_big(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><big>Test</big></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="big">Test</text:span>\n'

    def test_small(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><small>Test</small></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="small">Test</text:span>\n'

    def test_cite(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><cite>Test</cite></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Citation">Test</text:span>\n'

    def test_dfn(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><dfn>Test</dfn></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Citation">Test</text:span>\n'

    def test_var(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><var>Test</var></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Citation">Test</text:span>\n'

    def test_q(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><q>Test</q></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '<?xml version="1.0" encoding="utf-8"?>\n"Test"\n'

    def test_ins(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ins>Test</ins></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:span xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="underline">Test</text:span>
"""


if __name__ == '__main__':
    unittest.main()
