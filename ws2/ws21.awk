BEGIN {
	FS = ","
}
{
	if ($17 >= 10.0) {
		freqtips[$14]++
	}
}
END {
	for (tipamnt in freqtips) {
		print tipamnt, freqtips[tipamnt]
	}
}
