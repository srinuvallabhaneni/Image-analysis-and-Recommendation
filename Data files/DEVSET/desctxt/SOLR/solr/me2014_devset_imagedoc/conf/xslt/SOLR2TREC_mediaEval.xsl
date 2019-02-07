<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="text" indent="no" />
    <xsl:template match="/">
        <xsl:variable name="topic" select="/response/lst[@name='responseHeader']/lst[@name='params']/str[@name='topic']"/>
        <xsl:variable name="run" select="/response/lst[@name='responseHeader']/lst[@name='params']/str[@name='run']"/>
        <xsl:for-each select="response/result/doc">
            <xsl:value-of select="$topic"/><xsl:text>    Q0	</xsl:text>
            <xsl:value-of select="str[@name='id']"/><xsl:text>    </xsl:text>
            <xsl:value-of select="position()"/><xsl:text>    </xsl:text>
            <xsl:value-of select="float[@name='score']"/><xsl:text>	</xsl:text>
            <xsl:value-of select="$run"/><xsl:call-template name="Newline"></xsl:call-template>
            
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="Newline">
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
</xsl:stylesheet>
