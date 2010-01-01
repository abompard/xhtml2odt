#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from lxml import etree
from . import xhtml2odt

class TableElements(unittest.TestCase):
    """
    Style is determined by cell position:
        __________
        |A1|B1|C1|
        |A2|B2|C2|
        |A3|B3|C3|
        ^^^^^^^^^^
        __________
        |A4|B4|C4|
        ^^^^^^^^^^
    """

    def test_table1(self):
        """Classic full table"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
                <td>Cell 3</td>
              </tr>
              <tr>
                <td>Cell 4</td>
                <td>Cell 5</td>
                <td>Cell 6</td>
              </tr>
              <tr>
                <td>Cell 7</td>
                <td>Cell 8</td>
                <td>Cell 9</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="3"/> \s*
                             <table:table-row> \s* # -------- Line 1

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-A1">
                             <text:p [^>]* >Cell[ ]1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-B1">
                             <text:p [^>]* >Cell[ ]2</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-C1">
                             <text:p [^>]* >Cell[ ]3</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 2

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-A2">
                             <text:p [^>]* >Cell[ ]4</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-B2">
                             <text:p [^>]* >Cell[ ]5</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C2">
                             <text:p [^>]* >Cell[ ]6</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 3

                             <table:table-cell [^>]* # ---- Cell 7
                             table:style-name="table-default.cell-A3">
                             <text:p [^>]* >Cell[ ]7</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 8
                             table:style-name="table-default.cell-B3">
                             <text:p [^>]* >Cell[ ]8</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 9
                             table:style-name="table-default.cell-C3">
                             <text:p [^>]* >Cell[ ]9</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             </table:table>
                             """, str(odt), re.X)

    def test_table_oneline(self):
        """One-line table"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
                <td>Cell 3</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="3"/> \s*
                             <table:table-row> \s* # -------- Line 1

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell[ ]1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-B4">
                             <text:p [^>]* >Cell[ ]2</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell[ ]3</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_caption(self):
        """Test <caption> tag alone"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <caption>Caption</caption>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        assert odt.count('<text:p text:style-name="Caption">Table <text:sequence text:ref-name="refTable0" text:name="Table" text:formula="ooow:Table+1" style:num-format="1">1</text:sequence>: Caption</text:p>') > 0

    def test_table_caption_td(self):
        """Test <caption> tags with td tags"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <caption>Caption</caption>
              <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert str(odt).count('table:style-name="table-default.cell-A4"') > 0
        assert str(odt).count('table:style-name="table-default.cell-A4"') > 0

    def test_table_th(self):
        """Test <th> tags alone"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <th>Cell 1</th>
                <th>Cell 2</th>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-header-rows> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-H-A4">
                             <text:p [^>]* >Cell[ ]1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C4">
                             <text:p [^>]* >Cell[ ]2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_th_td(self):
        """Test <th> tags with <td> tags"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <th>Cell1</th>
                <th>Cell2</th>
              </tr>
              <tr>
                <td>Cell3</td>
                <td>Cell4</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-header-rows> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-H-A1">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C1">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*

                             <table:table-row> \s*
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A3">
                             <text:p [^>]* >Cell3</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C3">
                             <text:p [^>]* >Cell4</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_thead_no_tbody(self):
        """Test <thead> tag without <tbody>"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <thead>
                <tr>
                  <th>Cell1</th>
                  <th>Cell2</th>
                </tr>
              </thead>
              <tr>
                <td>Cell3</td>
                <td>Cell4</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-header-rows> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-H-A4">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C4">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*

                             <table:table-row> \s*
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell3</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell4</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_tfoot_no_tbody(self):
        """Test <tfoot> tag without <tbody>"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tfoot>
                <tr>
                  <td>Cell1</td>
                  <td>Cell2</td>
                </tr>
              </tfoot>
              <tr>
                <td>Cell3</td>
                <td>Cell4</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-F-A4">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-F-C4">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s*
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell3</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell4</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_tbody(self):
        """Test <tbody> tag"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tbody>
                <tr>
                  <td>Cell1</td>
                  <td>Cell2</td>
                </tr>
              </tbody>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_header_text_style(self):
        """Test text style inside <th> tags"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <th>Cell</th>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        print odt
        assert odt.count('<text:p text:style-name="Table_20_Heading">Cell</text:p>') > 0

    def test_table_single_cell(self):
        """Test single-cell tables (pretty useless if you ask me)"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr>
                <td>Cell</td>
              </tr>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="1"/> \s*
                             <table:table-row> \s* # -------- Line

                             <table:table-cell [^>]* # ---- Cell
                             table:style-name="table-default.cell-single">
                             <text:p [^>]* >Cell</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_thead_tbody(self):
        """Test <thead> tag with <tbody>"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <thead>
                <tr>
                  <th>Cell1</th>
                  <th>Cell2</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Cell3</td>
                  <td>Cell4</td>
                </tr>
              </tbody>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-header-rows> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-H-A4">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C4">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*

                             <table:table-row> \s*
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell3</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell4</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)

    def test_table_tfoot_tbody(self):
        """Test <tfoot> tag with <tbody>"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tfoot>
                <tr>
                  <td>Cell1</td>
                  <td>Cell2</td>
                </tr>
              </tfoot>
              <tbody>
                <tr>
                  <td>Cell3</td>
                  <td>Cell4</td>
                </tr>
              </tbody>
            </table>
        </html>
        """
        odt = xhtml2odt(html)
        # remove namespaces
        odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
        # remove comments
        odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
        print odt
        assert re.search(r"""
                             <table:table \s+ table:style-name="table-default"> \s*
                             <table:table-column \s+ table:number-columns-repeated="2"/> \s*
                             <table:table-row> \s*

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-F-A4">
                             <text:p [^>]* >Cell1</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-F-C4">
                             <text:p [^>]* >Cell2</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s*
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A4">
                             <text:p [^>]* >Cell3</text:p>
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C4">
                             <text:p [^>]* >Cell4</text:p>
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table>
                             """, str(odt), re.X)



if __name__ == '__main__':
    unittest.main()


