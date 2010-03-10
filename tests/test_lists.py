#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class ListElements(unittest.TestCase):

    def test_ul1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ul><li>Test</li></ul></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test</text:p>
  </text:list-item>
</text:list>
"""

    def test_ol1(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ol><li>Test</li></ol></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Numbering_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-number">Test</text:p>
  </text:list-item>
</text:list>
"""

    def test_ul2(self):
        """<ul> with two <li> inside"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ul><li>Test1</li><li>Test2</li></ul></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test1</text:p>
  </text:list-item>
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test2</text:p>
  </text:list-item>
</text:list>
"""

    def test_ul_ul(self):
        """<ul> with another <ul> inside"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ul><li>Test1</li><li><ul><li>Test2</li></ul></li></ul></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet">Test1</text:p>
  </text:list-item>
  <text:list-item>
    <text:p text:style-name="list-item-bullet"/>
    <text:list text:style-name="List_20_1">
      <text:list-item>
        <text:p text:style-name="list-item-bullet">Test2</text:p>
      </text:list-item>
    </text:list>
  </text:list-item>
</text:list>
"""

    def test_ul_ol(self):
        """<ul> with an <ol> inside"""
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><ul><li><ol><li>Test2</li></ol></li></ul></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
  <text:list-item>
    <text:p text:style-name="list-item-bullet"/>
    <text:list text:style-name="Numbering_20_1">
      <text:list-item>
        <text:p text:style-name="list-item-number">Test2</text:p>
      </text:list-item>
    </text:list>
  </text:list-item>
</text:list>
"""

    def test_dl(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><dl><dt>Term1</dt><dd>Def1</dd><dt>Term2</dt><dd>Def2</dd></dl></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt).count('table:number-columns-repeated="2"') == 1
        assert str(odt).count('</table:table-row>') == 2
        assert str(odt).count('</table:table-cell>') == 4

    def test_ul_in_dl(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><dl><dt>Term1</dt><dd>Def1<ul><li>Def1-LI</li></ul></dd></dl></html>'
        odt = xhtml2odt(html)
        print odt
        target = """
      <text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Text_20_body">Def1</text:p>
      <text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
        <text:list-item>
          <text:p text:style-name="list-item-bullet">Def1-LI</text:p>
        </text:list-item>
      </text:list>
"""
        assert str(odt).count(target) == 1


if __name__ == '__main__':
    unittest.main()
