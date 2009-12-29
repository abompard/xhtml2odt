"""
Unit tests for the stylesheet
"""

import os
from lxml import etree

def xhtml2odt(html, root_url="http://localhost", heading_minus_level="0"):
    main_dir = os.path.dirname(os.path.dirname(__file__))
    xslt_doc = etree.parse(os.path.join(main_dir, "xsl", "xhtml2odt.xsl"))
    transform = etree.XSLT(xslt_doc)
    html = etree.fromstring(html)
    root_url = etree.XSLT.strparam(root_url)
    odt = transform(html, root_url=root_url,
                    heading_minus_level=heading_minus_level)
    return odt
