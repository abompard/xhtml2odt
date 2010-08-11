#!/bin/bash

# XHTML2ODT -- Minimalist bash-script to run the stylesheets
#
# Project URL: http://xhtml2odt.org
# Copyright (C) 2009-2010 Aurelien Bompard
# License: GNU LGPL version 2.1 or later:
#          http://www.gnu.org/licenses/lgpl-2.1.html
#
# This script has no remote or local image support, no keywords, and in general
# no advanced features such as those of the PHP and Python scripts. Its purpose
# is to demonstrate the simplest use of the stylesheets, in a language many can
# understand.
#
# Requires: unzip, tidy, xsltproc

INSTALL_PATH="."

if [ $# -ne 3 ]; then
    echo "Usage: $0 <html-input-file> <odt-output-file> <odt-template-file>"
    exit 2
fi

htmlfile="$1"
odtfile="$2"
templatefile="$3"

if [ ! -f "$htmlfile" ]; then
    echo "Can't find input file: $htmlfile. Aborting." >&2
    exit 1
fi

if [ ! -f "$templatefile" ]; then
    echo "Can't find template file: $templatefile. Aborting." >&2
    exit 1
fi

if [ ! -d "$INSTALL_PATH/xsl" ]; then
    echo "Can't find the stylesheets in $INSTALL_PATH/xsl. Aborting" >&2
    exit 1
fi

# Unzip the template
tmpdir=`mktemp -d --tmpdir xhtml2odt-XXXX`
trap "rm -rf $tmpdir" EXIT
unzip -q -d $tmpdir/odt $templatefile

# Clean up the HTML
tidy -quiet -asxhtml -utf8 $htmlfile > $tmpdir/tidied.html
if [ $? -ne 0 ]; then
    echo "Tidy could not clean up the XHTML, aborting." >&2
    exit 1
fi

# Convert the XHTML
xsltproc $INSTALL_PATH/xsl/xhtml2odt.xsl $tmpdir/tidied.html \
    > $tmpdir/converted.xml
if [ $? -ne 0 ]; then
    echo "Impossible to convert the XHTML to ODT, aborting." >&2
    exit 1
fi
sed -i -e 's/<?xml version="1.0" encoding="utf-8"?>//' $tmpdir/converted.xml

# Add it to the template
sed -i -e 's,</office:text>.*</office:body>.*</office:document-content>,,' $tmpdir/odt/content.xml
cat $tmpdir/converted.xml >> $tmpdir/odt/content.xml
echo "</office:text></office:body></office:document-content>" >> $tmpdir/odt/content.xml

# Add missing styles and fonts
xsltproc $INSTALL_PATH/xsl/styles.xsl $tmpdir/odt/content.xml \
    > $tmpdir/odt/content.new.xml
mv $tmpdir/odt/content.new.xml $tmpdir/odt/content.xml
xsltproc $INSTALL_PATH/xsl/styles.xsl $tmpdir/odt/styles.xml \
    > $tmpdir/odt/styles.new.xml
mv $tmpdir/odt/styles.new.xml $tmpdir/odt/styles.xml

# Rebuild the zip file
pushd $tmpdir/odt >/dev/null
zip -q -r ../output.odt .
popd >/dev/null
mv $tmpdir/output.odt $odtfile

echo "The converted document has been written to $odtfile"
