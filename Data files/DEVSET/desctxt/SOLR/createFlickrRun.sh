#!/bin/bash


INDX=$1
TXTTOPICFILE=$2

rm solr_${INDX}.run

SAVEIFS=$IFS
IFS="|"
while read TOPIC LAT LONG WIKI QUERY; do 
 echo "read: <$TOPIC> <$LAT> <$LONG> <$WIKI> <$QUERY>"
 QUERYEscaped="$(perl -MURI::Escape -e 'print uri_escape($ARGV[0]);' "$QUERY")"

 curl http://localhost:8983/$INDX/select?q=*%3A*\&fq=poi%3A%22$QUERYEscaped%22\&rows=50\&sort=rank+asc\&fl=id,score\&topic=$TOPIC\&run=solr_${INDX}\&wt=xslt\&tr=SOLR2TREC_mediaEval.xsl >> flickr_${INDX}.run
done<$TXTTOPICFILE
IFS=$SAVEIFS
