<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="xml" version="1.0"/>

    <xsl:template match="/">
        <cookbook version="46">
            <xsl:for-each select="files/file">
                <xsl:apply-templates select="document(@path)/cookbook"/>
            </xsl:for-each>
        </cookbook>
    </xsl:template>

    <xsl:template match="cookbook">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="node()" name="copy">
        <xsl:copy>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>