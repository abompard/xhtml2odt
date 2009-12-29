#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from lxml import etree
from . import xhtml2odt

class GenericTests(unittest.TestCase):

    def test_unknown(self):
        html = '<html xmlns="http://www.w3.org/1999/xhtml"><unknown-tag unknown-attribute="foobar"/></html>'
        odt = xhtml2odt(html)
        print odt
        assert str(odt) == """<?xml version="1.0" encoding="utf-8"?>
<unknown-tag xmlns="http://www.w3.org/1999/xhtml" unknown-attribute="foobar"/>
"""


if __name__ == '__main__':
    unittest.main()
