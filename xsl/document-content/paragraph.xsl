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
	version="1.0"
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
	office:class="text"
	office:version="1.0">


<xsl:template match="h:p">
	<xsl:choose>
		<xsl:when test="
			child::h:ul|
			child::h:ol|
			child::h:blockquote|
			child::h:pre|
			child::h:screen
			">
			<!-- continue without text:p creation to child element -->
			
			<!-- when in this block is some text, display it in paragraph -->
			<!-- this is not functional
			<text:p>
				<xsl:value-of select="string(.)"/>
			</text:p>
			-->
			<!-- call template for each found element -->
			<xsl:for-each select="*">
				<xsl:apply-templates select="."/>
			</xsl:for-each>
		</xsl:when>
		<xsl:otherwise>
			<xsl:call-template name="paragraph"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<xsl:template name="paragraph">
	
	<xsl:variable name="position" select="position()"/>
	<xsl:variable name="position_div" select="position() div 2"/>
	<xsl:variable name="parent-previous" select="count(../preceding-sibling::node())"/>
	<xsl:variable name="nodes-in-previous" select="count(../preceding-sibling::li[$position_div]/*)"/>
	
	<text:p>
		
		<xsl:attribute name="text:style-name">
			<xsl:choose>
				
				<!-- deep magic part -->
				<xsl:when test="parent::h:ul|parent::h:ol">
					<xsl:choose>
						
						<!-- if paragraph is first in listitem                                 -->
						<!-- this paragraph is as title of listitem                            -->
						<xsl:when test="$position=2">
							<xsl:choose>
								<!-- very very very ugly hack :) but works very good :))))       -->
								<!-- http://blogs.msdn.com/asanto/archive/2004/09/08/226663.aspx -->
								<xsl:when test="$parent-previous = 1">para-list-begin</xsl:when>
								
								<!-- my very nice hack                                           -->
								
								<!-- when previous listitem has more than one element            -->
								
								<xsl:when test="$nodes-in-previous>1">para-list-padding</xsl:when>
								
								
								<xsl:when test="../../@spacing='compact'">para-list-compact</xsl:when>
								<xsl:when test="parent::h:ol/@spacing='compact'">para-list-compact</xsl:when>
								<xsl:when test="parent::h:ul/@spacing='compact'">para-list-compact</xsl:when>
								<xsl:otherwise>para-list-padding</xsl:otherwise>
							</xsl:choose>
						</xsl:when>
						
						<!-- all next paragraph in listitem -->
						<xsl:otherwise>
							<!--<xsl:text>para-padding</xsl:text>-->
							<xsl:choose>
								<xsl:when test="../../@spacing='compact'">para-list-compact</xsl:when>
								<xsl:otherwise>list-item</xsl:otherwise>
							</xsl:choose>
							
						</xsl:otherwise>
						
					</xsl:choose>
				</xsl:when>
				
				
				<xsl:when test="parent::h:blockquote">Quotations</xsl:when>
				
                <xsl:when test="contains(@style,'text-align:') and contains(@style,'center')">
                    <xsl:text>center</xsl:text>
                </xsl:when>

				<xsl:otherwise>Text_20_body</xsl:otherwise>
				
			</xsl:choose>
		</xsl:attribute>
		
		<xsl:apply-templates/>
		
	</text:p>
	
</xsl:template>


</xsl:stylesheet>
