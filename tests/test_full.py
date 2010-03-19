#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import unittest
from lxml import etree
from . import xhtml2odt

full_test_cleanup = re.compile('draw:name="imageobject-id\d+"')

class Full(unittest.TestCase):

    def _run_full_test(self, testid):
        tests_data = os.path.join(os.path.dirname(__file__), "data")
        html_file = open(os.path.join(tests_data, "%s.xhtml" % testid))
        html = html_file.read()
        html_file.close()
        xml_file = open(os.path.join(tests_data, "%s.xml" % testid))
        xml = xml_file.read()
        xml_file.close()
        odt = str(xhtml2odt(html))
        xml = full_test_cleanup.sub("", xml)
        odt = full_test_cleanup.sub("", odt)
        #xml_file = open(os.path.join(tests_data, "%s.xml.gen" % testid), "w")
        #xml_file.write(odt)
        #xml_file.close()
        assert odt == xml

    def test_full_1(self):
        return self._run_full_test(1)

    def test_full_2(self):
        return self._run_full_test(2)

    def test_full_3(self):
        return self._run_full_test(3)

if __name__ == '__main__':
    unittest.main()
