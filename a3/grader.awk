# Seperates the fields by comma
BEGIN {
	FS = ","
}

# Calculates the average grade for each student and classifies them as Pass (average ≥ 70) or Fail.
# (Must use a user-defined function to calculate the average.)

function average(total, count){
	return total / count
}

# Skips the header row and starts at Number of Records greater than 1

NR > 1 {
	total = 0
	count = 0

	# Gets the Total Score and the count of fields
	# Starts at 3 to skip the ID and Name
	# Goes from 3 to the end of the Number of Fields

	for (i = 3; i <= NF; i++) {
		total += $i
		count++
	}

	# Uses the Function to get the Average
	# Sets status equal to Pass or Fail

	avg = average(total, count)
	status = (avg >= 70) ? "Pass" : "Fail"

	# Stores all the values in arrays

	id = $1
	name = $2
	ids[id] = id
	scores[id] = total
	avgs[id] = avg
	statuses[id] = status
	names[id] = name

	# Gets the Highest Score and The Name of the Student

	if (total > highest_score || highest_score == "") {
		highest_score = total
		highest_name = name
	}

	# Gets the Lowest Score and the Name of the Student

	if (total < lowest_score || lowest_score == "") {
		lowest_score = total
		lowest_name = name
	}
}

# Prints the output in a nice format

END {
	print ""
	print "|----------|-----------|-------------|------------|"
	print "|   Name   |   Total   |   Average   |   Status   |"
	print "|----------|-----------|-------------|------------|"
	for(id in ids) {
		printf "| %-8s | %-9d | %-11.3f | %-10s |\n", names[id], scores[id], avgs[id], statuses[id]
	}
	print "|----------|-----------|-------------|------------|"
	print ""
	print "|-------------|-----------|"
	print "| Top Student | Max Score |"
	print "|-------------|-----------|"
	printf "| %-11s | %-9d |\n", highest_name, highest_score
	print "|-------------|-----------|"
	print ""
	print "|----------------|--------------|"
	print "| Lowest Student | Lowest Score |"
	print "|----------------|--------------|"
	printf "| %-14s | %-12d |\n", lowest_name, lowest_score
	print "|----------------|--------------|"
	print ""
}
