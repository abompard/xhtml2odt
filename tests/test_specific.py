#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class SpecificTrac(unittest.TestCase):

    def test_underline(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><span class="underline">Test</span></p></html>'
        odt = xhtml2odt(html)
        odt = str(odt).replace(' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"', '')
        odt = odt.replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
        self.assertEquals(odt, """<text:p text:style-name="Text_20_body">
  <text:span text:style-name="underline">Test</text:span>
</text:p>
""")

    def test_underline_outside_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><span class="underline">Test</span></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt),"")


class SpecificPygments(unittest.TestCase):

    def _test_mapping(self, css, odtstyle):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="%s">Test</span></pre></div></html>' % css
        odt = xhtml2odt(html)
        odt = str(odt).replace(' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"', '')
        odt = odt.replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
        self.assertEquals(odt, """<text:p text:style-name="Source_20_Code">
  <text:span text:style-name="%s">Test</text:span>
</text:p><text:p text:style-name="Text_20_body"/>\n""" % odtstyle)

    def test_highlight_k(self):
        self._test_mapping("k", "strong")

    def test_highlight_kn(self):
        self._test_mapping("kn", "strong")

    def test_highlight_nc(self):
        self._test_mapping("nc", "syntax-highlight.class")

    def test_highlight_nf(self):
        self._test_mapping("nf", "syntax-highlight.function")

    def test_highlight_nt(self):
        self._test_mapping("nt", "syntax-highlight.tag")

    def test_highlight_na(self):
        self._test_mapping("na", "syntax-highlight.attr")

    def test_highlight_nb(self):
        self._test_mapping("nb", "syntax-highlight.builtin")

    def test_highlight_nn(self):
        self._test_mapping("nn", "syntax-highlight.namespace")

    def test_highlight_ne(self):
        self._test_mapping("ne", "syntax-highlight.exception")

    def test_highlight_nv(self):
        self._test_mapping("nv", "syntax-highlight.var")

    def test_highlight_bp(self):
        self._test_mapping("bp", "syntax-highlight.builtin.pseudo")

    def test_highlight_s(self):
        self._test_mapping("s", "syntax-highlight.string")

    def test_highlight_sd(self):
        self._test_mapping("sd", "syntax-highlight.string")

    def test_highlight_si(self):
        self._test_mapping("si", "syntax-highlight.string")

    def test_highlight_se(self):
        self._test_mapping("se", "syntax-highlight.string")

    def test_highlight_sb(self):
        self._test_mapping("sb", "syntax-highlight.string")

    def test_highlight_s2(self):
        self._test_mapping("s2", "syntax-highlight.string")

    def test_highlight_mi(self):
        self._test_mapping("mi", "syntax-highlight.number")

    def test_highlight_mf(self):
        self._test_mapping("mf", "syntax-highlight.number")

    def test_highlight_o(self):
        self._test_mapping("o", "strong")

    def test_highlight_ow(self):
        self._test_mapping("ow", "strong")

    def test_highlight_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="p">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        odt = str(odt).replace(' xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"', '')
        odt = odt.replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
        self.assertEquals(odt, """<text:p text:style-name="Source_20_Code">Test</text:p>"""
                               """<text:p text:style-name="Text_20_body"/>\n""")

    def test_highlight_c(self):
        self._test_mapping("c", "syntax-highlight.comment")

    def test_highlight_err(self):
        self._test_mapping("err", "syntax-highlight.error")


if __name__ == '__main__':
    unittest.main()
