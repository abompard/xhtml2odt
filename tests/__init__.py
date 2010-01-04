"""
Unit tests for the stylesheet
"""

import os
from lxml import etree

def xhtml2odt(html, params={}):
    """Run the transformation. Used by all the unit tests."""
    main_dir = os.path.dirname(os.path.dirname(__file__))
    xslt_doc = etree.parse(os.path.join(main_dir, "xsl", "xhtml2odt.xsl"))
    transform = etree.XSLT(xslt_doc)
    html = etree.fromstring(html)
    for key, value in params.iteritems():
        params[key] = etree.XSLT.strparam(value)
    odt = transform(html, **params)
    return odt
