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
        </recipe>
    </xsl:template>

    <xsl:template match="head">
        <title><xsl:value-of select="title"/></title>
        <xsl:apply-templates select="categories/cat"/>
        <xsl:apply-templates select="yield"/>
    </xsl:template>

    <xsl:template match="categories/cat">
        <category><xsl:value-of select="."/></category>
    </xsl:template>

    <xsl:template match="yield">
        <quantity><xsl:value-of select="."/></quantity>
    </xsl:template>
</xsl:stylesheet>
