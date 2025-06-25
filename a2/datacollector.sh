#!/bin/bash

echo -n "Please enter a URL to a CSV dataset: "
read url
echo $url
curl -O $url

ZIPFILE=$(ls -t *.zip | head -1)

if [ -f "$ZIPFILE" ]; then
	echo "Downloaded File: $ZIPFILE"
	echo "Unzipping $ZIPFILE"
	unzip -o "$ZIPFILE"
	find . -cnewer $ZIPFILE -name "*.csv" | cut -c 3- > extracted_files.txt
else
	echo "Error: Zip file not found"
	exit 1
fi

echo "Creating Summary"
