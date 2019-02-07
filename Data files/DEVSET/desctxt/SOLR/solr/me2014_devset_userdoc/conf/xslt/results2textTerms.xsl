<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text" encoding="utf-8" indent="no"/>
						
<xsl:template match="/">
<xsl:for-each select="response/lst[@name='termVectors']/lst">
  <xsl:value-of select="str[@name='uniqueKey']"/><xsl:text> </xsl:text>
  <xsl:for-each select="lst[@name='text']/lst">
  <xsl:text>"</xsl:text><xsl:value-of select="@name"/><xsl:text>" </xsl:text>
  <xsl:value-of select="int[@name='tf']"/> <xsl:text> </xsl:text>
  <xsl:value-of select="int[@name='df']"/> <xsl:text> </xsl:text>
  <xsl:value-of select="double[@name='tf-idf']"/><xsl:text> </xsl:text>
</xsl:for-each> 
<xsl:text>&#10;</xsl:text>
</xsl:for-each>
</xsl:template>

<xsl:template name="Newline">
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
</xsl:stylesheet>