#!/usr/bin/env python

"""
    xhtml2odt - XHTML to ODT XML transformation.
    Copyright (C) 2009-2010 Aurelien Bompard

This script can convert a wiki page to the OpenDocument Text (ODT) format,
standardized as ISO/IEC 26300:2006, and the native format of office suites such
as OpenOffice.org, KOffice, and others.

It uses a template ODT file which will be filled with the converted content of
the exported Wiki page.

Based on the work on docbook2odt, by Roman Fordinal
http://open.comsultia.com/docbook2odf/

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import tempfile
import shutil
import re
import os
import sys
import zipfile
import urllib2
import urlparse
import subprocess
from glob import glob
from StringIO import StringIO
from optparse import OptionParser

import tidy
from lxml import etree
from PIL import Image

#pylint#: disable-msg=E0611,C0301,C0111

INSTALL_PATH = "."

INCH_TO_CM = 2.54
CHARSET = "utf-8"


class ODTExportError(Exception): pass

class HTMLFile(object):

    def __init__(self, options):
        self.options = options
        self.html = ""

    def read(self):
        in_file = open(self.options.input)
        self.html = in_file.read()
        in_file.close()
        self.cleanup()
        if self.options.htmlid:
            self.select_id()

    def cleanup(self):
        tidy_options = dict(output_xhtml=1, add_xml_decl=1, indent=1,
                            tidy_mark=0, #input_encoding=str(self.charset),
                            output_encoding='utf8', doctype='auto',
                            wrap=0, char_encoding='utf8')
        self.html = str(tidy.parseString(self.html, **tidy_options))
        # Replace nbsp with entity
        # http://www.mail-archive.com/analog-help@lists.meer.net/msg03670.html
        self.html = self.html.replace("&nbsp;", "&#160;") \
                             .replace("\xa0", "&#160;")
        # Tidy creates newlines after <pre> (by indenting)
        self.html = re.sub('<pre([^>]*)>\n', '<pre\\1>', self.html)

    def select_id(self):
        html_tree = etree.fromstring(self.html)
        selected = html_tree.xpath("//*[@id='%s']" % self.options.htmlid)
        self.html = etree.tostring(selected[0], method="html")


class ODTFile(object):
    """Handles the conversion and production of an ODT file"""

    def __init__(self, options):
        self.options = options
        self.template_dirs = []
        if options.tpldir:
            self.template_dirs.append(options.tpldir)
        self.template_dirs.append(
            os.path.join(INSTALL_PATH, "styles")
        )
        self.xml = {
            "content": "",
            "styles": "",
        }
        self.tmpdir = tempfile.mkdtemp(prefix="xhtml2odt-")
        self.styles = {}
        self.autostyles = {}
        self.style_name_re = re.compile('style:name="([^"]+)"') 
        self.fonts = {}

    def open(self):
        self.zfile = zipfile.ZipFile(self.options.template, "r")
        for name in self.zfile.namelist():
            fname = os.path.join(self.tmpdir, name)
            if not os.path.exists(os.path.dirname(fname)):
                os.makedirs(os.path.dirname(fname))
            if name[-1] == "/":
                if not os.path.exists(fname):
                    os.mkdir(fname)
                continue
            fname_h = open(fname, "w")
            fname_h.write(self.zfile.read(name))
            fname_h.close()
        for xmlfile in self.xml:
            self.xml[xmlfile] = self.zfile.read("%s.xml" % xmlfile)

    def import_xhtml(self, xhtml):
        odt = self.xhtml_to_odt(xhtml)
        self.insert_content(odt)
        self.add_styles()

    def xhtml_to_odt(self, xhtml):
        xsl_dir = os.path.join(INSTALL_PATH, 'xsl')
        xslt_doc = etree.parse(os.path.join(xsl_dir, "xhtml2odt.xsl"))
        transform = etree.XSLT(xslt_doc)
        xhtml = self.handle_images(xhtml)
        xhtml = etree.fromstring(xhtml) # must be valid xml at this point
        params = {
            "root_url": "/",
            "heading_minus_level": str(self.options.top_header_level - 1),
        }
        if self.options.verbose:
            params["debug"] = "1"
        if self.options.img_width:
            params["img_default_width"] = etree.XSLT.strparam(
                                            self.options.img_width)
        if self.options.img_height:
            params["img_default_height"] = etree.XSLT.strparam(
                                            self.options.img_height)
        odt = transform(xhtml, **params)
        return str(odt).replace('<?xml version="1.0" encoding="utf-8"?>','')

    def handle_images(self, xhtml):
        # Handle local images
        xhtml = re.sub('<img [^>]*src="([^"]+)"',
                      self.handle_local_img, xhtml)
        # Handle remote images
        if self.options.with_network:
            xhtml = re.sub('<img [^>]*src="(https?://[^"]+)"',
                          self.handle_remote_img, xhtml)
        return xhtml

    def handle_local_img(self, img_mo):
        log("handling local image: %s" % img_mo.group(1), self.options.verbose)
        src = img_mo.group(1)
        if src.count("://") and not src.startswith("file://"):
            # This is an absolute link, don't touch it
            return img_mo.group()
        if src.startswith("file://"):
            filename = src[7:]
        elif src.startswith("/"):
            filename = src
        else: # relative link
            filename = os.path.join(os.path.dirname(self.options.input), src)
        if os.path.exists(filename):
            return self.handle_img(img_mo.group(), src, filename)
        if src.startswith("file://") or not self.options.url \
                or not self.options.with_network:
            # There's nothing we can do here
            return img_mo.group()
        newsrc = urlparse.urljoin(self.options.url, os.path.normpath(src))
        try:
            tmpfile = self.download_img(newsrc)
        except urllib2.HTTPError:
            log("Failed getting %s" % newsrc, self.options.verbose)
            return img_mo.group()
        ret = self.handle_img(img_mo.group(), src, tmpfile)
        os.remove(tmpfile)
        return ret

    def handle_remote_img(self, img_mo):
        log('handling remote image: %s' % img_mo.group(), self.options.verbose)
        src = img_mo.group(1)
        try:
            tmpfile = self.download_img(src)
        except urllib2.HTTPError:
            return img_mo.group()
        ret = self.handle_img(img_mo.group(), src, tmpfile)
        os.remove(tmpfile)
        return ret

    def download_img(self, src):
        """
        Download the image to a temporary location
        """
        log('Downloading image: %s' % src, self.options.verbose)
        # TODO: proxy support
        remoteimg = urllib2.urlopen(src)
        tmpimg_fd, tmpfile = tempfile.mkstemp()
        tmpimg = os.fdopen(tmpimg_fd, 'w')
        tmpimg.write(remoteimg.read())
        tmpimg.close()
        remoteimg.close()
        return tmpfile

    def handle_img(self, full_tag, src, filename):
        log('Importing image: %s' % filename, self.options.verbose)
        if not os.path.exists(filename):
            raise ODTExportError('Image "%s" is not readable or does not exist' % filename)
        # TODO: generate a filename (with tempfile.mkstemp) to avoid weird filenames.
        #       Maybe use img.format for the extension
        if not os.path.exists(os.path.join(self.tmpdir, "Pictures")):
            os.mkdir(os.path.join(self.tmpdir, "Pictures"))
        shutil.copy(filename, os.path.join(self.tmpdir, "Pictures",
                                           os.path.basename(filename)))
        newsrc = "Pictures/%s" % os.path.basename(filename)
        try:
            img = Image.open(filename)
        except IOError:
            log('Failed to identify image: %s' % filename, self.options.verbose)
        else:
            width, height = img.size
            log('Detected size: %spx x %spx' % (width, height), self.options.verbose)
            width = width / float(self.options.img_dpi) * INCH_TO_CM
            height = height / float(self.options.img_dpi) * INCH_TO_CM
            newsrc += '" width="%scm" height="%scm' % (width, height)
        return full_tag.replace(src, newsrc)

    def insert_content(self, content):
        if self.options.replace_keyword and \
            self.xml["content"].count(self.options.replace_keyword) > 0:
            # TODO: this creates an empty line before and after the
            # replace_keyword. It's not optimal, I should use a regexp to
            # remove the previous opening <text:p> tag and the corresponding
            # closing tag.
            self.xml["content"] = self.xml["content"].replace(
                self.options.replace_keyword,
                '</text:p>%s<text:p text:style-name="Text_20_body">' % content)
        else:
            self.xml["content"] = self.xml["content"].replace(
                '</office:text>',
                content + '</office:text>')

    def import_style(self, style, is_mainstyle=False):
        style_name_mo = self.style_name_re.search(style)
        name = style_name_mo.group(1)
        if name in self.styles:
            return # already added
        if self.xml["content"].count('style:name="%s"' % name) > 0 or \
           self.xml["styles"].count('style:name="%s"' % name) > 0:
            return # already present in the template
        if is_mainstyle:
            self.styles[name] = style
        else:
            self.autostyles[name] = style

    def import_font(self, font):
        style_name_mo = self.style_name_re.search(font)
        name = style_name_mo.group(1)
        if name in self.fonts:
            return # already added
        if self.xml["styles"].count('<style:font-face style:name="%s"' % name) > 0 or \
            self.xml["content"].count('<style:font-face style:name="%s"' % name) > 0:
            return # already present in the template
        self.fonts[name] = font

    def add_styles(self):
        odtstyle = ODTStyle(self.template_dirs)
        odtstyle.add_styles(self.xml["content"], self.import_style,
                            self.import_font)

    def compile(self):
        # autostyles
        if self.autostyles:
            autostyles = "\n".join(self.autostyles.values())
            for xmlfile in ["content", "styles"]:
                if self.xml[xmlfile].count("<office:automatic-styles/>") > 0:
                    self.xml[xmlfile] = self.xml[xmlfile].replace(
                        "<office:automatic-styles/>",
                        "<office:automatic-styles>%s</office:automatic-styles>" %
                        autostyles)
                else:
                    self.xml[xmlfile] = self.xml[xmlfile].replace(
                        "</office:automatic-styles>",
                        "%s</office:automatic-styles>" % autostyles)
        if self.styles:
            styles = "\n".join(self.styles.values())
            self.xml["styles"] = self.xml["styles"].replace(
                "</office:styles>", "%s</office:styles>" % styles)
        if self.fonts:
            fonts = "\n".join(self.fonts.values())
            for xmlfile in ["content", "styles"]:
                self.xml[xmlfile] = self.xml[xmlfile].replace(
                    "</office:font-face-decls>",
                    "%s</office:font-face-decls>" % fonts)
        # Store the new content
        for xmlfile in self.xml:
            xmlf = open(os.path.join(self.tmpdir, "%s.xml" % xmlfile), "w")
            xmlf.write(self.xml[xmlfile])
            xmlf.close()

    def _build_zip(self, document):
        newzf = zipfile.ZipFile(document, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(self.tmpdir):
            for file in files:
                realpath = os.path.join(root, file)
                internalpath = os.path.join(root.replace(self.tmpdir, ""), file)
                newzf.write(realpath, internalpath)
        newzf.close()

    def save(self, output=None):
        self.compile()
        if output:
            document = output
        else:
            document = StringIO()
        self._build_zip(document)
        shutil.rmtree(self.tmpdir)
        if not output:
            return document.getvalue()


class ODTStyle(object):
    """
    This class contains the ODT style library
    """
    # pylint#: disable-msg=C0103

    def __init__(self, template_dirs):
        self.template_dirs = template_dirs
        self.style_name_re = re.compile('style:name="([^"]+)"') 
        self.need_font_re = re.compile('font-name="([^"]+)"')

    def _build_style_lib(self):
        """build a library of available styles"""
        template_files = self._build_templates_list()
        style_lib = {}
        for style_file in template_files.values():
            style_tpl = open(style_file)
            style_xml = style_tpl.read()
            style_tpl.close()
            style = self._build_style(style_xml)
            if not style:
                continue
            style_lib[style["name"]] = style
        return style_lib

    def _build_templates_list(self):
        """select the preferred template (used-defined or default)"""
        template_files = {}
        for template_dir in self.template_dirs:
            for style_file in glob(os.path.join(template_dir, "*.txt")):
                basename = os.path.basename(style_file)
                if basename not in template_files:
                    template_files[basename] = style_file
        return template_files

    def _build_style(self, style_xml):
        style_name_mo = self.style_name_re.search(style_xml)
        if not style_name_mo:
            return False
        style = {
            "name": style_name_mo.group(1),
            "xml": style_xml,
        }
        is_mainstyle = (style_xml.count("style:display-name=") > 0)
        style["mainstyle"] = is_mainstyle
        need_font = self.need_font_re.search(style_xml)
        if need_font:
            style["need_font"] = need_font.group(1)
        return style


    def add_styles(self, content_xml, import_style_callback,
                                      import_font_callback):
        """
        Add the missing styles using callbacks
        """
        style_lib = self._build_style_lib()
        for stylename in style_lib:
            if content_xml.count('style-name="%s"' % stylename) == 0:
                continue # style is not used
            style_xml = style_lib[stylename]["xml"]
            is_mainstyle = style_lib[stylename]["mainstyle"]
            import_style_callback(style_xml, is_mainstyle)
            if "need_font" in style_lib[stylename]:
                font_name = style_lib[stylename]["need_font"]
                font_xml = style_lib[font_name]["xml"]
                import_font_callback(font_xml)


def log(msg, verbose=False):
    if verbose:
        sys.stderr.write(msg+"\n")

def get_options():
    usage = "usage: %prog [options] -i input -o output -t template.odt"
    parser = OptionParser(usage=usage)
    parser.add_option("-i", "--input", dest="input",
                      help="Read the html from this file")
    parser.add_option("-o", "--output", dest="output",
                      help="Location of the output ODT file")
    parser.add_option("-t", "--template", dest="template",
                      help="Location of the template ODT file")
    parser.add_option("-u", "--url", dest="url",
                      help="Use this URL for relative links")
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=False,
                      help="Show what's going on")
    parser.add_option("--img-default-width", dest="img_width",
                      help="Default image width (default is 8cm)")
    parser.add_option("--img-default-height", dest="img_height",
                      help="Default image height (default is 6cm)")
    parser.add_option("--dpi", dest="img_dpi", type="int", default=96,
                      help="Screen resolution in DPI (Dots Per Inch)")
    parser.add_option("--no-network", dest="with_network",
                      action="store_false", default=True,
                      help="Download remote images")
    parser.add_option("--replace", dest="replace_keyword", default="ODT-INSERT",
                      help="Keyword to replace in the ODT template")
    parser.add_option("--tpldir", dest="tpldir",
                      help="Override templates directory")
    parser.add_option("--top-header-level", dest="top_header_level",
                      type="int", default="1",
                      help="Level of highest header in the HTML")
    parser.add_option("--html-id", dest="htmlid",
                      help="Only export from this element")
    options, args = parser.parse_args()
    if len(args) > 0:
        parser.error("illegal arguments: %s"% ", ".join(args))
    if not options.input:
        parser.error("No input provided")
    if not options.output:
        parser.error("No output provided")
    if not options.template:
        parser.error("No ODT template provided")
    if not os.path.exists(options.input):
        parser.error("Can't find input file: %s" % options.input)
    if not os.path.exists(options.template):
        parser.error("Can't find template file: %s" % options.template)
    return options, args

def main():
    options, args = get_options()
    htmlfile = HTMLFile(options)
    htmlfile.read()
    odtfile = ODTFile(options)
    odtfile.open()
    odtfile.import_xhtml(htmlfile.html)
    odtfile.save(options.output)

if __name__ == '__main__':
    main()

