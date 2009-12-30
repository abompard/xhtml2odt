<?xml version="1.0" encoding="utf-8"?>
<!--
	
	xhtml2odt - XHTML to ODT XML transformation.
    Copyright (C) 2009 Aurelien Bompard
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



<xsl:template match="h:blockquote">
	<!-- special formatting is defined in paragraph -->
	<xsl:apply-templates/>
</xsl:template>

<xsl:template match="h:hr">
	<text:p text:style-name="Horizontal_20_Line"/>
</xsl:template>

<xsl:template match="h:pre">
    <text:p>
        <xsl:attribute name="text:style-name">
            <xsl:text>Preformatted_20_Text</xsl:text>
        </xsl:attribute>
        <xsl:call-template name="pre.line">
            <xsl:with-param name="content" select="string(.)"/>
        </xsl:call-template>
	</text:p>
</xsl:template>

<xsl:template name="pre.line">
	<xsl:param name="content"/>
		<xsl:choose>
			<xsl:when test="contains($content, '&#10;')">
                <xsl:value-of select="substring-before($content, '&#10;')"/>
                <text:line-break/>
				<xsl:call-template name="pre.line">
					<xsl:with-param name="content" select="substring-after($content, '&#10;')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
                <xsl:value-of select="string($content)"/>
			</xsl:otherwise>
		</xsl:choose>
</xsl:template>

<xsl:template match="h:address">
	<!-- special formatting is defined in paragraph -->
	<xsl:call-template name="paragraph"/>
</xsl:template>

<xsl:template match="h:center">
	<!-- special formatting is defined in paragraph -->
	<xsl:call-template name="paragraph"/>
</xsl:template>

</xsl:stylesheet>
