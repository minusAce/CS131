#!/bin/bash

echo -n "Please enter a URL to a CSV dataset: "
read url
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

{
while read -r csv_file; do
	if [ -f "$csv_file" ]; then
	echo ""
	echo "# Feature Summary for $csv_file"
	echo ""
	echo "## Feature Index and Names"
	head -1 "$csv_file" | sed -e 's/"//g' -e 's/;/\n/g' | awk '{print NR ". " $0}'
	echo ""
	echo "## Statistics (Numerical Features)"
	echo "| Index | Feature           | Min  | Max  | Mean  | StdDev |"
	echo "|-------|-------------------|------|------|-------|--------|"
	num_cols=$(head -1 "$csv_file" | sed 's/"//g' | awk -F';' '{print NF}')
	for ((i=1; i<=num_cols; i++)); do
		header=$(head -1 "$csv_file" | sed 's/"//g' | cut -d ';' -f $i)
		num_check=$(sed -n '2p' "$csv_file" | cut -d ';' -f $i)
		if [[ $num_check =~ ^[0-9\.]+$ ]]; then
			awk -F';' -v col="$i" -v header="$header" '
                		NR > 1 {
                    			val = $col
                        		if (min == "" || val < min) min = val
                        		if (max == "" || val > max) max = val
                        		sum += val
                        		sumsq += val * val
                        		count++
                		}
                		END {
                    			if (count > 0) {
                        			mean = sum / count
                        			stddev = sqrt((sumsq - (sum * sum) / count) / count)
                        			printf "| %-5d | %-17s | %-4.2f | %-4.2f | %-5.3f | %-6.3f |\n", col, header, min, max, mean, stddev
                        		}
                		}' "$csv_file"
		else
        		echo "$header is not numeric"
    		fi
	done
    fi
done < extracted_files.txt
} > summary.md

rm extracted_files.txt
