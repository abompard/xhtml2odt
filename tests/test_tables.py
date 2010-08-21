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
                             table:style-name="table-default.cell-A1"> \s*
                             <text:p [^>]* >Cell[ ]1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-B1"> \s*
                             <text:p [^>]* >Cell[ ]2</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-C1"> \s*
                             <text:p [^>]* >Cell[ ]3</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 2

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell[ ]4</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-B2"> \s*
                             <text:p [^>]* >Cell[ ]5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell[ ]6</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 3

                             <table:table-cell [^>]* # ---- Cell 7
                             table:style-name="table-default.cell-A3"> \s*
                             <text:p [^>]* >Cell[ ]7</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 8
                             table:style-name="table-default.cell-B3"> \s*
                             <text:p [^>]* >Cell[ ]8</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 9
                             table:style-name="table-default.cell-C3"> \s*
                             <text:p [^>]* >Cell[ ]9</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*

                             </table:table> \s*
                             """, str(odt), re.X)

    def test_table_oneline(self):
        """<table> tag: only one line"""
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
                             table:style-name="table-default.cell-A4"> \s*
                             <text:p [^>]* >Cell[ ]1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-B4"> \s*
                             <text:p [^>]* >Cell[ ]2</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-C4"> \s*
                             <text:p [^>]* >Cell[ ]3</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
                             """, str(odt), re.X)

    def test_table_onecol(self):
        """<table> tag: only one column"""
        html = """<html xmlns="http://www.w3.org/1999/xhtml">
            <table>
              <tr><td>Cell 1</td></tr>
              <tr><td>Cell 2</td></tr>
              <tr><td>Cell 3</td></tr>
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

                             <table:table-row> \s* # -------- Line 1
                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-C1"> \s*
                             <text:p [^>]* >Cell[ ]1</text:p> \s*
                             </table:table-cell> \s*
                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 2
                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell[ ]2</text:p> \s*
                             </table:table-cell> \s*
                             </table:table-row> \s*

                             <table:table-row> \s* # -------- Line 3
                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-C3"> \s*
                             <text:p [^>]* >Cell[ ]3</text:p> \s*
                             </table:table-cell> \s*
                             </table:table-row> \s*

                             </table:table> \s*
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
              <tr>
                <td>Cell5</td>
                <td>Cell6</td>
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
                             table:style-name="table-default.cell-H-A1"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C1"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*
                             <table:table-row> \s* # ---- Line 1

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell3</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell4</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Line 2

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-A3"> \s*
                             <text:p [^>]* >Cell5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-C3"> \s*
                             <text:p [^>]* >Cell6</text:p> \s*
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
              <tr>
                <td>Cell5</td>
                <td>Cell6</td>
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
                             table:style-name="table-default.cell-H-A1"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C1"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*
                             <table:table-row> \s* # ---- Line 1

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell3</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell4</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Line 2

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-A3"> \s*
                             <text:p [^>]* >Cell5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C3"> \s*
                             <text:p [^>]* >Cell6</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
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
              <tr>
                <td>Cell5</td>
                <td>Cell6</td>
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
                             <table:table-row> \s* # ---- Line 1

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A1"> \s*
                             <text:p [^>]* >Cell3</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C1"> \s*
                             <text:p [^>]* >Cell4</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Line 2

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell6</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Footer

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-F-A3"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-F-C3"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
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
                             table:style-name="table-default.cell-A4"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-C4"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
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

    def test_table_text_style(self):
        """Test text style inside <td> tags"""
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
        print odt
        assert odt.count('<text:p text:style-name="Table_20_Contents">Cell</text:p>') > 0

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
                             table:style-name="table-default.cell-single"> \s*
                             <text:p [^>]* >Cell</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
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
                <tr>
                  <td>Cell5</td>
                  <td>Cell6</td>
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
                             table:style-name="table-default.cell-H-A1"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-H-C1"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table-header-rows> \s*
                             <table:table-row> \s* # ---- Line 1

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell3</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell4</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Line 2

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-A3"> \s*
                             <text:p [^>]* >Cell5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C3"> \s*
                             <text:p [^>]* >Cell6</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
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
                <tr>
                  <td>Cell5</td>
                  <td>Cell6</td>
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
                             <table:table-row> \s* # ---- Line 1

                             <table:table-cell [^>]* # ---- Cell 3
                             table:style-name="table-default.cell-A1"> \s*
                             <text:p [^>]* >Cell3</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 4
                             table:style-name="table-default.cell-C1"> \s*
                             <text:p [^>]* >Cell4</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Line 2

                             <table:table-cell [^>]* # ---- Cell 5
                             table:style-name="table-default.cell-A2"> \s*
                             <text:p [^>]* >Cell5</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 6
                             table:style-name="table-default.cell-C2"> \s*
                             <text:p [^>]* >Cell6</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             <table:table-row> \s* # ---- Footer

                             <table:table-cell [^>]* # ---- Cell 1
                             table:style-name="table-default.cell-F-A3"> \s*
                             <text:p [^>]* >Cell1</text:p> \s*
                             </table:table-cell> \s*

                             <table:table-cell [^>]* # ---- Cell 2
                             table:style-name="table-default.cell-F-C3"> \s*
                             <text:p [^>]* >Cell2</text:p> \s*
                             </table:table-cell> \s*

                             </table:table-row> \s*
                             </table:table> \s*
                             """, str(odt), re.X)

    def test_td_containing_ul(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><table><tr><td>Text1<ul><li>Text2</li></ul>Text3</td></tr></table></html>'
        odt = xhtml2odt(html)
        print odt
        target = """
      <text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Table_20_Contents">Text1</text:p>
      <text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="List_20_1">
        <text:list-item>
          <text:p text:style-name="list-item-bullet">Text2</text:p>
        </text:list-item>
      </text:list>
      <text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" text:style-name="Table_20_Contents">Text3</text:p>
"""
        assert str(odt).count(target) == 1



if __name__ == '__main__':
    unittest.main()


