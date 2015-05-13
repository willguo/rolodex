import re
import json

def encapsulate(first_name_match, last_name_match, name_match, color_match, zip_match, phone_match):
	if first_name_match and last_name_match and color_match and zip_match and phone_match \
		or name_match and color_match and zip_match and phone_match:
		# Name portion.
		first_name = None
		last_name = None
		if name_match:
			name = name_match.group("elem")
			name_array = name.rsplit(" ", 1)
			if len(name_array) < 2:
				# Add to error list.
				error_list.append(str(linecount))
			first_name = name_array[0]
			last_name = name_array[1]
		else:
			first_name = first_name_match.group("elem")
			last_name = last_name_match.group("elem")
		# Color code portion.
		color = color_match.group("elem")
		# Zip code portion.
		zipcode = zip_match.group("elem")
		# Phone number portion.
		phone = re.sub(" ", "-", (phone_match.group("elem")))
		phone = re.sub("\(", "", phone)
		phone = re.sub("\)", "", phone)
		# Replace the following.
		print (first_name + " " + last_name + " " + zipcode + " " + color + " " + phone)
		return [first_name, last_name, color, zipcode, phone]
		# return True
	else:
		return False

def normalize():
	# Open up the file to be read.
	datafile = open('practice.in', 'r')

	# Error list to keep track of errors found in the input data.
	error_list = []

	# Patterns to match with.
	# Pattern to be used for first name and full name matches.
	pattern1 = re.compile("(?P<elem>^[a-zA-Z'\. ]+$)")
	# Pattern to be used with last name matches.
	pattern2 = re.compile("(?P<elem>^[a-zA-Z']+$)")
	# Pattern to be used with color matches.
	pattern3 = re.compile("(?P<elem>^[a-zA-Z ]+$)")
	# Pattern to be used for matching zip codes.
	pattern4 = re.compile("(?P<elem>^[0-9]{5}$)")
	# Pattern to be used to match dash-delimited phone numbers.
	pattern5 = re.compile("(?P<elem>^\([0-9]{3}\)-[0-9]{3}-[0-9]{4}$)")
	# Pattern to be used to match space-delimited phone numbers.
	pattern6 = re.compile("(?P<elem>^[0-9]{3} [0-9]{3} [0-9]{4}$)")

	# Keep track of line numbers (for errors).
	linecount = 0

	# Iterate through lines in the input file.
	for line in datafile:
		line_components = line.split(", ")
		if len(line_components) == 4:
			# Check format number 2.
			print ("4 COMPONENTS")
			# print (line_components[2])
			name_match = pattern1.match(line_components[0])
			color_match = pattern3.match(line_components[1])
			zip_match = pattern4.match(line_components[2])
			phone_match = pattern6.match(line_components[3])
			# print ("TYPE " + type(name_match).__name__)

			success = encapsulate(None, None, name_match, color_match, zip_match, phone_match)

			# If match is found, then capture match and split into first and last name.
			if success:
				print ("SUCCESS")
			else:
				print ("FAILURE")
				error_list.append(str(linecount))

		elif len(line_components) == 5:
			# Check format numbers 1, 3.
			print ("5 COMPONENTS")
			last_name_match1 = pattern2.match(line_components[0])
			first_name_match1 = pattern1.match(line_components[1])
			color_match1 = pattern3.match(line_components[3])
			zip_match1 = pattern4.match(line_components[4])
			phone_match1 = pattern5.match(line_components[2])

			last_name_match2 = pattern2.match(line_components[1])
			first_name_match2 = pattern1.match(line_components[0])
			color_match2 = pattern3.match(line_components[4])
			zip_match2 = pattern4.match(line_components[2])
			phone_match2 = pattern6.match(line_components[3])
			
			# Check format number 1.
			success1 = encapsulate(first_name_match1, last_name_match1, None, color_match1, zip_match1, phone_match1);
			# Check format number 3.
			success2 = encapsulate(first_name_match2, last_name_match2, None, color_match2, zip_match2, phone_match2);

			if success1:
				print ("SUCCESS")
			elif success2:
				print ("SUCCESS")
			else:
				print ("FAILURE")
				error_list.append(str(linecount))

		else:
			# Add to line to error array (number of arguments do not match).
			error_list.append(str(linecount))

		linecount += 1
	
	print ("FAIL " + ', '.join(error_list))

	# pattern = 

	# Test would be to try names that are not in English (tilda n)
	# UNICODE PROPERTIES ARE NOT SUPPORTED IN PYTHON WITHOUT USE OF EXTERNAL LIBRARIES.
	
	return 0