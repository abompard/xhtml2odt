<?xml version="1.0" encoding="utf-8"?>
<!--
    
    xhtml2odt - XHTML to ODT XML transformation.
    Copyright (C) 2009 Aurelien Bompard
    Inspired by the work on docbook2odt, by Roman Fordinal
    http://open.comsultia.com/docbook2odf/
    
    License: LGPL v2.1 or later <http://www.gnu.org/licenses/lgpl-2.1.html>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA  02110-1301  USA

-->
<xsl:stylesheet
    xmlns:h="http://www.w3.org/1999/xhtml"
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" 
    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"
    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"
    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"
    xmlns:math="http://www.w3.org/1998/Math/MathML"
    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"
    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"
    xmlns:dom="http://www.w3.org/2001/xml-events"
    xmlns:xforms="http://www.w3.org/2002/xforms"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0"
    version="1.0">


<!--
     Code highlighting
     This is incomplete, see http://pygments.org/docs/tokens/
-->

<!-- Keyword -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='k']" mode="inparagraph">
    <text:span text:style-name="strong">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Keyword.Namespace -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='kn']" mode="inparagraph">
    <text:span text:style-name="strong">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Class -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='nc']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.class">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Function -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='nf']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.function">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Tag -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='nt']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.tag">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Attribute -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='na']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.attr">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Builtin -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='nb']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.builtin">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Name.Namespace -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='nn']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.namespace">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Punctuation -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='p']" mode="inparagraph">
    <xsl:apply-templates mode="inparagraph"/>
</xsl:template>

<!-- Name.Builtin.Pseudo -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='bp']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.builtin.pseudo">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- String -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='s']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.string">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Operator -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='o']" mode="inparagraph">
    <text:span text:style-name="strong">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Comment -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='c']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.comment">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Generic.Error -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='err']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.error">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Number.Integer -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='mi']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.int">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

<!-- Number.Float -->
<xsl:template match="h:div[@class='code']/h:pre/h:span[@class='mf']" mode="inparagraph">
    <text:span text:style-name="syntax-highlight.float">
        <xsl:apply-templates mode="inparagraph"/>
    </text:span>
</xsl:template>

</xsl:stylesheet>
