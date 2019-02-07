#!/bin/bash

DATAFILE=$1
FOLDERNAMESFILE=$2


OLDIFS=$IFS
IFS="	";
i=0
cp $DATAFILE temp0.txt
while read poi folder; do
 echo "$i"
 echo "POI: $poi"
 echo "folder: $folder"
 sed "s/^\($poi\)/$folder $poi/" temp$i.txt > temp$((i+1)).txt
 rm temp$i.txt
 i=$((i+1))
done < $FOLDERNAMESFILE
mv temp$i.txt ${DATAFILE%.*}.wFolderNames.txt
