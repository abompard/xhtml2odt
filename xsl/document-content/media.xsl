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


<xsl:template match="h:img">
    
    <!-- @align                                                  -->
    <!-- @contentwidth                                           -->
    <!-- @contentheight                                          -->
    <!-- @fileref                                                -->
    <!-- @format                                                 -->
    <!-- @scale                                                  -->
    <!-- @scalefit                                               -->
    <!-- @valign                                                 -->
    <!-- @width                                                  -->
    <!-- @depth                                                  -->
    
    <xsl:element name="draw:frame">

        <xsl:choose>
            <xsl:when test="substring-before(@width,'cm') &lt; 2 and substring-before(@height,'cm') &lt; 2">
                <xsl:attribute name="text:anchor-type">as-char</xsl:attribute>
                <xsl:attribute name="draw:style-name">image-inline</xsl:attribute>
            </xsl:when>
            <xsl:otherwise>
                <xsl:attribute name="text:anchor-type">paragraph</xsl:attribute>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:attribute name="draw:name">imageobject-<xsl:value-of select="generate-id()"/></xsl:attribute>
        
        <xsl:choose>
            <xsl:when test="@width|@height">
                <xsl:attribute name="svg:width"><xsl:value-of select="@width"/></xsl:attribute>
                <xsl:attribute name="svg:height"><xsl:value-of select="@height"/></xsl:attribute>
            </xsl:when>
            <xsl:otherwise>
                <!-- In OpenDocument svg:width and height must be defined. Use defaults here -->
                <xsl:attribute name="svg:width"><xsl:value-of select="$img_default_width"/></xsl:attribute>
                <xsl:attribute name="style:rel-width">scale</xsl:attribute>
                <xsl:attribute name="svg:height"><xsl:value-of select="$img_default_height"/></xsl:attribute>
                <xsl:attribute name="style:rel-height">scale</xsl:attribute>
            </xsl:otherwise>
        </xsl:choose>
        
        <xsl:attribute name="svg:y"><xsl:value-of select="$para.padding"/></xsl:attribute>
        
        <xsl:attribute name="draw:z-index">1</xsl:attribute>
        <xsl:element name="draw:image">
            <xsl:attribute name="xlink:href"><xsl:value-of select="@src"/></xsl:attribute>
            <xsl:attribute name="xlink:type">simple</xsl:attribute>
            <xsl:attribute name="xlink:show">embed</xsl:attribute>
            <xsl:attribute name="xlink:actuate">onLoad</xsl:attribute>
        </xsl:element>

        <xsl:element name="svg:title"><xsl:value-of select="@alt"/></xsl:element>
        
    </xsl:element>
    
</xsl:template>



</xsl:stylesheet>
