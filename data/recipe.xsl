<?xml version="1.0"?>
<!-- recipe.xsl -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" version="1.0"/>

    <xsl:template match="/">
        <cookbook version="46">
            <source>
                <xsl:apply-templates select="recipeml/meta[contains('DC.Creator DC.Source DC.Identifier DC.Publisher DC.Date DC.Rights', @name)]"/>
            </source>
            <xsl:apply-templates select="recipeml/recipe"/>
        </cookbook>
    </xsl:template>

    <xsl:template match="meta[contains('DC.Creator DC.Source DC.Identifier DC.Publisher DC.Date DC.Rights', @name)]">
        <li>
            <xsl:value-of select="substring-after(@name, 'DC.')"/>
            <xsl:text>: </xsl:text>
            <xsl:value-of select="@content"/>
        </li>
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

    <!-- split the recipe steps by double empty lines -->
    <xsl:template match="step" name="split">
        <xsl:param name="pText" select="."/>
        <xsl:if test="$pText">
            <li><xsl:value-of select="normalize-space(substring-before(concat($pText,'&#xa;&#xa;'),'&#xa;&#xa;'))"/></li>
            <xsl:call-template name="split">
                <xsl:with-param name="pText" select="substring-after($pText, '&#xa;&#xa;')"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <!-- end directions -->
</xsl:stylesheet>
