#!/bin/bash


CORE=$1
FILES=$2

URL=http://localhost:8983/$CORE/update

curl $URL --data-binary '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'

curl $URL --data-binary '<commit/>' -H 'Content-type:text/xml; charset=utf-8'

echo "FILES: $FILES"

files=`ls $FILES`

echo "new files: $files"

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for f in $files; do 
  fPath="$FILES/$f"
  echo Posting file $fPath to $URL 
  curl $URL --data-binary @$fPath -H 'Content-type:text/xml; charset=utf-8' 
  echo "" 
done 
IFS=$SAVEIFS

#send the commit command to make sure all the changes are flushed and visible
curl $URL --data-binary '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
echo
