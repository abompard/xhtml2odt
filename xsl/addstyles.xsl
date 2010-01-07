<?xml version="1.0" encoding="UTF-8"?>
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
    exclude-result-prefixes="office xsl dc text style table draw fo xlink meta number svg chart dr3d math form script dom xforms xsd xsi presentation h"
    version="1.0">
    
<!-- SETTINGS -->
<xsl:decimal-format name="staff" digit="D" />
<xsl:output method="xml" indent="yes" omit-xml-declaration="no" encoding="utf-8"/>
<!--<xsl:strip-space elements="*"/>-->
<!--<xsl:preserve-space elements=""/>-->


<xsl:include href="param.xsl"/>


<xsl:template match="/">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="office:automatic-styles">
    <office:automatic-styles>
        <!-- copy the existing styles -->
        <xsl:for-each select="child::*">
            <xsl:copy>
                <xsl:copy-of select="@*"/>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:for-each>
        <!-- add missing styles -->
        <xsl:call-template name="addmissingstyles">
            <xsl:with-param name="mainstyle"/>
        </xsl:call-template>
    </office:automatic-styles>
</xsl:template>

<xsl:template match="office:styles">
    <office:styles>
        <!-- copy the existing styles -->
        <xsl:for-each select="child::*">
            <xsl:copy>
                <xsl:copy-of select="@*"/>
                <xsl:apply-templates/>
            </xsl:copy>
        </xsl:for-each>
        <!-- add missing styles -->
        <xsl:call-template name="addmissingstyles">
            <xsl:with-param name="mainstyle" select="1"/>
        </xsl:call-template>
    </office:styles>
</xsl:template>

<xsl:template name="addmissingstyles">
    <xsl:param name="mainstyle"/>
    <xsl:for-each select="//office:body/descendant::*">
        <xsl:for-each select="@*">
            <xsl:if test="local-name(.) = 'style-name'">
                <xsl:comment>Found style: <xsl:value-of select="string(.)"/></xsl:comment>
                <xsl:call-template name="addstyle">
                    <xsl:with-param name="stylename" select="string(.)"/>
                    <xsl:with-param name="mainstyle" select="$mainstyle"/>
                </xsl:call-template>
            </xsl:if>
        </xsl:for-each>
    </xsl:for-each>
</xsl:template>

<xsl:template name="addstyle">
    <xsl:param name="stylename"/>
    <xsl:param name="mainstyle"/>
    <xsl:comment>Template addstyle called with <xsl:value-of select="$stylename"/></xsl:comment>
    <xsl:if test="not(//office:automatic-styles/style:style[@style:name = $stylename])
                  and not(//office:styles/style:style[@style:name = $stylename])">
        <xsl:comment>Style <xsl:value-of select="$stylename"/> is not already there</xsl:comment>
        <xsl:for-each select="document('styles.xml')/styles/style:style[@style:name = $stylename]">
            <xsl:comment>Found style <xsl:value-of select="$stylename"/> in the lib</xsl:comment>
            <xsl:if test="($mainstyle and @style:display-name) or (not($mainstyle) and not(@style:display-name))">
                <xsl:comment>Style <xsl:value-of select="$stylename"/> is of the right category</xsl:comment>
                <xsl:copy>
                    <xsl:copy-of select="@*"/>
                    <xsl:apply-templates/>
                </xsl:copy>
            </xsl:if>
        </xsl:for-each>
    </xsl:if>
</xsl:template>

<!-- Leave alone unknown tags -->
<xsl:template match="*">
    <xsl:copy>
        <xsl:copy-of select="@*"/>
        <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

</xsl:stylesheet>
