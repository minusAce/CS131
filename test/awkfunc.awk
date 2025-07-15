function find_min(num1, num2) {
	if (num1 < num2)
		return num1
	return num2
}

BEGIN {
	print "the min = ", find_min(10,20)
}
