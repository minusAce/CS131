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

while read -r csv_file; do
    if [ -f "$csv_file" ]; then
	echo ""
        echo "#Feature Summary for $csv_file"
	echo ""
	echo "##Feature Index and Names"
        head -1 "$csv_file" | tr -d '"' | tr ';' '\n' | nl -s '. '
	echo ""
	echo "## Statistics (Numerical Features)"
	num_cols=$(head -1 "$csv_file" | tr -d '"' | awk -F';' '{print NF}')
	for ((i=1; i<=num_cols; i++)); do
		header=$(head -1 "$csv_file" | tr -d '"' | cut -d ";" -f "$i")
		num_check=$(sed -n '2p' "$csv_file" | cut -d ";" -f "$i")
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
                        			printf "%s stats:\n", header
                        			printf "  Min: %.2f\n", min
                        			printf "  Max: %.2f\n", max
                        			printf "  Mean: %.3f\n", mean
                        			printf "  Std Dev: %.3f\n", stddev
                    			}
                		}' "$csv_file"
		else
        		echo "$header is not numeric"
    		fi
	done
    fi
done < extracted_files.txt
