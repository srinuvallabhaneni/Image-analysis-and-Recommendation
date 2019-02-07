#!/bin/bash

CORE=$1
FILE=$2

#First get the number of results
RESULTS=`curl http://localhost:8983/$CORE/select?q=*%3A* | grep -oe numFound=\"[^\"]*\" | cut -d"\"" -f2`

echo "Found : $RESULTS results"

STEP=10

echo "storing the first $STEP elements in a new file named $FILE"
curl http://localhost:8983/$CORE/select?q=*%3A*\&start=0\&rows=$STEP\&wt=xslt\&tr=results2textTerms.xsl\&indent=true\&qt=tvrh\&tv.all=true > $FILE

echo "Appending to $FILE all the other results"
for i in $(seq $STEP $STEP $RESULTS); do
 echo $i;
 curl http://localhost:8983/$CORE/select?q=*%3A*\&start=$i\&rows=$STEP\&wt=xslt\&tr=results2textTerms.xsl\&indent=true\&qt=tvrh\&tv.all=true >> $FILE
done


#for 
