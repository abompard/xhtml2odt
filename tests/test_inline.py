#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class InlineElements(unittest.TestCase):

    def test_em(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><em>Test</em></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="emphasis">Test</text:span>
</text:p>
'''

    def test_i(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><i>Test</i></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="emphasis">Test</text:span>
</text:p>
'''

    def test_strong(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><strong>Test</strong></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="strong">Test</text:span>
</text:p>
'''

    def test_b(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><b>Test</b></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="strong">Test</text:span>
</text:p>
'''

    def test_b_and_i(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><b><i>Test</i></b></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="strong">
    <text:span text:style-name="emphasis">Test</text:span>
  </text:span>
</text:p>
'''


    def test_sub(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><sub>Test</sub></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="sub">Test</text:span>
</text:p>
'''

    def test_sup(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><sup>Test</sup></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="sup">Test</text:span>
</text:p>
'''

    def test_code(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><code>Test</code></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Teletype">Test</text:span>
</text:p>
'''

    def test_tt(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><tt>Test</tt></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Teletype">Test</text:span>
</text:p>
'''

    def test_samp(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><samp>Test</samp></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Teletype">Test</text:span>
</text:p>
'''

    def test_kbd(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><kbd>Test</kbd></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Teletype">Test</text:span>
</text:p>
'''

    def test_br(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><br/></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:line-break/>
</text:p>
'''

    def test_del(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><del>Test</del></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="strike">Test</text:span>
</text:p>
'''

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
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><big>Test</big></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="big">Test</text:span>
</text:p>
'''

    def test_small(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><small>Test</small></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="small">Test</text:span>
</text:p>
'''

    def test_cite(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><cite>Test</cite></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Citation">Test</text:span>
</text:p>
'''

    def test_dfn(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><dfn>Test</dfn></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Citation">Test</text:span>
</text:p>
'''

    def test_var(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><var>Test</var></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="Citation">Test</text:span>
</text:p>
'''

    def test_q(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><q>Test</q></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == '''<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">"Test"</text:p>
'''

    def test_ins(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><p><ins>Test</ins></p></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">
  <text:span text:style-name="underline">Test</text:span>
</text:p>
"""


if __name__ == '__main__':
    unittest.main()
