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
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="underline">Test</text:span>
</text:p>
""")

    def test_underline_outside_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><span class="underline">Test</span></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt),"")

    def test_highlight_k(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="k">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="strong">Test</text:span>
</text:p>
""")

    def test_highlight_nc(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="nc">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="syntax-highlight.class">Test</text:span>
</text:p>
""")

    def test_highlight_p(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="p">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">Test</text:p>
""")

    def test_highlight_nf(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="nf">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="syntax-highlight.function">Test</text:span>
</text:p>
""")

    def test_highlight_bp(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="bp">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="syntax-highlight.builtin.pseudo">Test</text:span>
</text:p>
""")

    def test_highlight_s(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="s">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="syntax-highlight.string">Test</text:span>
</text:p>
""")

    def test_highlight_o(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><div class="code"><pre><span class="o">Test</span></pre></div></html>'
        odt = xhtml2odt(html)
        print odt
        self.assertEquals(str(odt), """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Preformatted_20_Text">
  <text:span text:style-name="strong">Test</text:span>
</text:p>
""")


if __name__ == '__main__':
    unittest.main()
