<?xml version="1.0"?>
<!-- transform.xsl -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" version="1.0"/>

    <xsl:template match="/">
        <cookbook version="46">
            <xsl:apply-templates select="recipeml/recipe"/>
            <xsl:call-template name="source"/>
        </cookbook>
    </xsl:template>

    <!--  meta  -->
    <xsl:template match="meta[contains('DC.Creator DC.Source DC.Identifier DC.Publisher DC.Date DC.Rights', @name)]">
        <li>
            <xsl:value-of select="substring-after(@name, 'DC.')"/>
            <xsl:text>: </xsl:text>
            <xsl:value-of select="@content"/>
        </li>
    </xsl:template>

    <xsl:template name="source">
        <source>
            <xsl:apply-templates select="recipeml/meta[contains('DC.Creator DC.Source DC.Identifier DC.Publisher DC.Date DC.Rights', @name)]"/>
            <xsl:apply-templates select="recipeml/recipe/head/source"/>
        </source>
    </xsl:template>
    <!--  end meta  -->

    <!--  recipe  -->
    <xsl:template match="recipe">
        <recipe>
            <xsl:apply-templates select="head"/>
            <xsl:apply-templates select="ingredients"/>
            <xsl:apply-templates select="directions"/>
        </recipe>
    </xsl:template>

    <!-- head -->
    <xsl:template match="head">
        <xsl:apply-templates select="title"/>
        <xsl:apply-templates select="subtitle"/>
        <xsl:apply-templates select="categories/cat"/>
        <xsl:apply-templates select="yield"/>
        <xsl:apply-templates select="preptime"/>
    </xsl:template>

    <xsl:template match="head/title">
        <title><xsl:apply-templates/></title>
    </xsl:template>

    <xsl:template match="subtitle">
        <description><xsl:apply-templates/></description>
    </xsl:template>

    <xsl:template match="cat">
        <category><xsl:value-of select="."/></category>
    </xsl:template>

    <xsl:template match="yield">
        <quantity><xsl:value-of select="."/></quantity>
    </xsl:template>

    <xsl:template match="source|note">
        <li><xsl:apply-templates/></li>
    </xsl:template>

    <xsl:template match="preptime">
        <xsl:choose>
            <xsl:when test="@type='preparation'">
                <preptime>
                    <xsl:apply-templates/>
                </preptime>
            </xsl:when>
            <xsl:when test="@type='cooking'">
                <cooktime>
                    <xsl:apply-templates/>
                </cooktime>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <!-- end head -->

    <!-- ingredients -->
    <xsl:template match="ingredients">
        <ingredient>
            <xsl:apply-templates select="ing-div|note|ing"/>
        </ingredient>
    </xsl:template>

    <xsl:template match="ing-div">
        <li>
            <xsl:text>Ingredient Group: </xsl:text>
            <xsl:apply-templates select="title"/>
            <xsl:if test="title and description">
                <xsl:text> (</xsl:text>
            </xsl:if>
            <xsl:apply-templates select="description"/>
            <xsl:if test="title and description">
                <xsl:text>)</xsl:text>
            </xsl:if>
        </li>
         <xsl:apply-templates select="note|ing"/>
    </xsl:template>

    <xsl:template match="ing">
        <li>
            <xsl:call-template name="space-between-children"/>
        </li>
    </xsl:template>

    <xsl:template match="alt-ing">
        <xsl:text>or </xsl:text>
        <xsl:call-template name="space-between-children"/>
    </xsl:template>
    <!-- end ingredients -->

    <!-- directions -->
    <xsl:template match="directions">
        <recipetext>
            <xsl:apply-templates select="step"/>
        </recipetext>
    </xsl:template>

    <xsl:template match="step" name="split">
        <!-- split the recipe steps by double empty lines -->
        <xsl:param name="pText" select="."/>
        <xsl:if test="$pText">
            <li><xsl:value-of select="normalize-space(substring-before(concat($pText,'&#xa;&#xa;'),'&#xa;&#xa;'))"/></li>
            <xsl:call-template name="split">
                <xsl:with-param name="pText" select="substring-after($pText, '&#xa;&#xa;')"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <!-- end directions -->

    <!--  common formatting  -->
    <xsl:template match="amt|size|modifier|time|temp|prep|qty|brandname|span|mfr|product|q1|q2|ing-note|title|description" name="space-between-children">
        <xsl:for-each select="text()|*">
            <xsl:apply-templates select="."/>
            <xsl:if test=".//text() and ./following-sibling::*//text()">
                <xsl:text> </xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="timeunit|tempunit|sep|unit|item">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="range">
        <xsl:apply-templates select="q1"/>
        <xsl:apply-templates select="sep"/>
        <xsl:if test="not(sep)">
            <xsl:text> - </xsl:text>
        </xsl:if>
        <xsl:apply-templates select="q2"/>
    </xsl:template>

    <xsl:template match="frac">
        <xsl:value-of select="n"/>
        <xsl:apply-templates select="sep"/>
        <xsl:if test="not(sep)">
            <xsl:text>/</xsl:text>
        </xsl:if>
        <xsl:value-of select="d"/>
    </xsl:template>
    <!--  end common formatting  -->
    <!--  end recipe  -->
</xsl:stylesheet>