<?xml version="1.0"?>
<!-- recipe.xsl -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" version="1.0"/>

    <xsl:template match="/">
        <cookbook version="46">
            <xsl:apply-templates select="recipeml/recipe"/>
        </cookbook>
    </xsl:template>

    <xsl:template match="recipe">
        <recipe>
            <xsl:apply-templates select="head"/>
            <xsl:apply-templates select="ingredients"/>
            <xsl:apply-templates select="directions"/>
        </recipe>
    </xsl:template>

    <!-- head -->
    <xsl:template match="head">
        <title><xsl:value-of select="title"/></title>
        <xsl:apply-templates select="categories/cat"/>
        <xsl:apply-templates select="yield"/>
    </xsl:template>

    <xsl:template match="cat">
        <category><xsl:value-of select="."/></category>
    </xsl:template>

    <xsl:template match="yield">
        <quantity><xsl:value-of select="."/></quantity>
    </xsl:template>
    <!-- end head -->

    <!-- ingredients -->
    <xsl:template match="ingredients">
        <ingredient>
            <xsl:apply-templates select="ing"/>
        </ingredient>
    </xsl:template>

    <xsl:template match="ing">
        <li>
            <xsl:apply-templates select="amt"/>
            <xsl:apply-templates select="item"/>
        </li>
    </xsl:template>

    <!-- amount -->
    <xsl:template match="amt">
        <xsl:apply-templates select="qty"/>
        <xsl:apply-templates select="unit"/>
    </xsl:template>

    <xsl:template match="qty">
        <xsl:value-of select="."/>
        <xsl:text> </xsl:text>
    </xsl:template>

    <xsl:template match="unit">
        <xsl:value-of select="."/>
        <xsl:if test="string(.)">
            <xsl:text> </xsl:text>
        </xsl:if>
    </xsl:template>
    <!-- end amount -->

    <xsl:template match="item">
        <xsl:value-of select="."/>
    </xsl:template>
    <!-- end ingredients -->

    <!-- directions -->
    <xsl:template match="directions">
        <recipetext>
            <xsl:apply-templates select="step"/>
        </recipetext>
    </xsl:template>

    <xsl:template match="step">
        <li><xsl:value-of select="normalize-space()"/></li>
    </xsl:template>
    <!-- end directions -->
</xsl:stylesheet>
