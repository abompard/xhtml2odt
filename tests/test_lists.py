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

    def test_ul3(self):
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


if __name__ == '__main__':
    unittest.main()
