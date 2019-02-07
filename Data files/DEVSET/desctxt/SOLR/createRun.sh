#!/bin/bash


INDX=$1
TXTTOPICFILE=$2

rm solr_${INDX}.run

SAVEIFS=$IFS
IFS="|"
while read TOPIC LAT LONG WIKI QUERY; do 
 echo "read: <$TOPIC> <$LAT> <$LONG> <$WIKI> <$QUERY>"
 QUERYEscaped="$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "$QUERY")"

 echo "curl http://localhost:8983/$INDX/select?q=$QUERYEscaped\&fq=poi%3A%22$QUERYEscaped%22\&rows=50\&fl=id,score\&topic=$TOPIC\&run=solr_${INDX}\&wt=xslt\&tr=SOLR2TREC_mediaEval.xsl >> solr_${INDX}.run"

 curl http://localhost:8983/$INDX/select?q=$QUERYEscaped\&fq=poi%3A%22$QUERYEscaped%22\&rows=50\&fl=id,score\&topic=$TOPIC\&run=solr_${INDX}\&wt=xslt\&tr=SOLR2TREC_mediaEval.xsl >> solr_${INDX}.run
done<$TXTTOPICFILE
IFS=$SAVEIFS
