# CSV Feature Summary Tool
## What this command does
This shell script automates the process of downloading, extracting, and analyzing a CSV dataset (typically inside a ZIP file from a URL). It generates a markdown report (summary.md) that includes:

A list of all features (columns) in the dataset

Basic statistics (min, max, mean, standard deviation) for numerical features

## How to use this command
Navigate to the directory containing the script.

Run the script using:

bash
Copy
Edit
./your_script_name.sh
When prompted, enter the URL to a ZIP file containing a CSV dataset.

The script will:

Download the ZIP file

Extract the CSV file(s)

Process each CSV file

Output a readable markdown summary to summary.md

Note: Ensure the CSV file is semicolon-separated (;) and that the first row contains headers.

# Demo
Below is a sample run of the script from a terminal:

bash
Copy
Edit
$ ./summary.sh
Please enter a URL to a CSV dataset: https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.zip
https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  478k  100  478k    0     0   728k      0 --:--:-- --:--:-- --:--:--  728k
Downloaded File: winequality-red.zip
Unzipping winequality-red.zip

# Feature Summary for winequality-red.csv

## Feature Index and Names
1. fixed acidity
2. volatile acidity
3. citric acid
4. residual sugar
5. chlorides
6. free sulfur dioxide
7. total sulfur dioxide
8. density
9. pH
10. sulphates
11. alcohol
12. quality

## Statistics (Numerical Features)
| Index | Feature           | Min  | Max  | Mean  | StdDev |
|-------|-------------------|------|------|-------|--------|
| 1     | fixed acidity      | 4.60 | 15.90 | 8.319 | 1.741  |
| 2     | volatile acidity   | 0.12 | 1.58 | 0.528 | 0.179  |
| 3     | citric acid        | 0.00 | 1.00 | 0.271 | 0.195  |
...
| 12    | quality            | 3.00 | 8.00 | 5.636 | 0.808  |
