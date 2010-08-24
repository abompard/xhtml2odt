"""
Unit tests for the stylesheet
"""

import os
import re
from lxml import etree

def xhtml2odt(html, params={}, no_cleanup=False):
    """Run the transformation. Used by all the unit tests."""
    main_dir = os.path.dirname(os.path.dirname(__file__))
    xslt_doc = etree.parse(os.path.join(main_dir, "xsl", "xhtml2odt.xsl"))
    transform = etree.XSLT(xslt_doc)
    html = etree.fromstring(html)
    for key, value in params.iteritems():
        params[key] = etree.XSLT.strparam(value)
    odt = transform(html, **params)
    if no_cleanup:
        return odt
    # remove namespaces
    odt = re.sub('(xmlns:[a-z0-9=:".-]+\s+)*', '', str(odt))
    # remove comments
    odt = re.sub('(<!--[a-z0-9=-]+-->)*', '', odt)
    # remove xml declaration
    odt = odt.replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
    # remove trailing newline
    if len(odt) > 0 and odt[-1] == "\n":
        odt = odt[:-1]
    return odt

def styles(odt, params={}):
    """Run the transformation. Used by all the unit tests."""
    main_dir = os.path.dirname(os.path.dirname(__file__))
    xslt_doc = etree.parse(os.path.join(main_dir, "xsl", "styles.xsl"))
    transform = etree.XSLT(xslt_doc)
    odt = etree.fromstring(odt)
    for key, value in params.iteritems():
        params[key] = etree.XSLT.strparam(value)
    return transform(odt, **params)

