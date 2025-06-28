# CSV Feature Summary Tool
## What this command does
This shell script automates the process of downloading, extracting, and analyzing a CSV dataset (typically inside a ZIP file from a URL). It generates a summary (summary.md) that includes:

  1. A list of all features (columns) in the dataset
  2. Basic statistics (min, max, mean, standard deviation) for numerical features

## How to use this command
Navigate to the directory containing the script.

Run the script using:

	./datacollector.sh

When prompted, enter the URL to a ZIP file containing a CSV dataset.

The script will:

  1. Download the ZIP file
  2. Extract the CSV file(s)
  3. Process the CSV file(s)
  4. Output the result to summary.md

# Demo
Below is a sample run of the script from a terminal:

	$ ./datacollector.sh
	Please enter a URL to a CSV dataset: https://archive.ics.uci.edu/static/public/186/wine+quality.zip
	https://archive.ics.uci.edu/static/public/186/wine+quality.zip
	  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
	100 91353    0 91353    0     0   326k      0 --:--:-- --:--:-- --:--:--  327k
	Downloaded File: wine+quality.zip
	Unzipping wine+quality.zip
	Archive:  wine+quality.zip
 	 inflating: winequality-red.csv     
 	 inflating: winequality-white.csv   
 	 inflating: winequality.names       
	$ cat summary.md 

	# Feature Summary for winequality-red.csv

	## Feature Index and Names
	1. fixed acidity
	2. volatile acidity
	3. citric acid
	...
	12. quality

	## Statistics (Numerical Features)
	| Index | Feature           | Min  | Max  | Mean  | StdDev |
	|-------|-------------------|------|------|-------|--------|
	| 1     | fixed acidity     | 4.60 | 15.90 | 8.320 | 1.741  |
	| 2     | volatile acidity  | 0.12 | 1.58 | 0.528 | 0.179  |
	| 3     | citric acid       | 0.00 | 1.00 | 0.271 | 0.195  |
	...
	| 12    | quality           | 3.00 | 8.00 | 5.636 | 0.807  |
