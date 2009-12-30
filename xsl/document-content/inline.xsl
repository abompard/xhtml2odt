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


<xsl:template match="h:a">
    <xsl:choose>
        <xsl:when test="h:img">
            <draw:a>
                <xsl:call-template name="link"/>
            </draw:a>
        </xsl:when>
        <xsl:otherwise>
            <text:a>
                <xsl:call-template name="link"/>
            </text:a>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="link">
    <xsl:attribute name="xlink:type"><xsl:text>simple</xsl:text></xsl:attribute>
    <xsl:attribute name="xlink:href">
        <xsl:choose>
            <xsl:when test="contains(@href, '#') and contains(@href,$root_url)">
                <xsl:text>#</xsl:text><xsl:value-of select="substring-after(@href,'#')"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="@href"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:attribute>
    <xsl:choose>
        <xsl:when test="@id">
            <text:bookmark-start>
                <xsl:attribute name="text:name">
                    <xsl:value-of select="@id"/>
                </xsl:attribute>
            </text:bookmark-start>
        </xsl:when>
    </xsl:choose>
    <xsl:apply-templates/>
    <xsl:choose>
        <xsl:when test="@id">
            <text:bookmark-end>
                <xsl:attribute name="text:name">
                    <xsl:value-of select="@id"/>
                </xsl:attribute>
            </text:bookmark-end>
        </xsl:when>
    </xsl:choose>
</xsl:template>


<xsl:template match="h:em|h:i">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>Emphasis</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>

<xsl:template match="h:strong|h:b">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>Strong_20_Emphasis</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>

<xsl:template match="h:sup">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>sup</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>

<xsl:template match="h:sub">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>sub</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>

<xsl:template match="h:code|h:tt">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>Teletype</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>

<xsl:template match="h:br">
    <text:line-break/>
</xsl:template>

<xsl:template match="h:del">
	<text:span>
		<xsl:attribute name="text:style-name">
            <xsl:text>Strike</xsl:text>
		</xsl:attribute>
		<xsl:apply-templates/>
	</text:span>
</xsl:template>


</xsl:stylesheet>
