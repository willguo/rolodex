import re
import json
import collections

def encapsulate(first_name_match, last_name_match, name_match, color_match, zip_match, phone_match):
	if first_name_match and last_name_match and color_match and zip_match and phone_match \
		or name_match and color_match and zip_match and phone_match:
		# Name portion.
		first_name = None
		last_name = None
		if name_match:
			name = name_match.group("elem")
			name_array = name.rsplit(" ", 1)
			# Add to error list if full name is less than 2 words.
			if len(name_array) < 2:
				return False
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
		return [color, first_name, last_name, phone, zipcode]
	else:
		return False

def normalize(input_file):
	# Open up the file to be read.
	datafile = open(str(input_file), 'r')

	# Dictionary to keep track of parsed data.
	dictionary = {}
	# List to keep track of JSON data.
	entries_list = []
	# Error list to keep track of errors found in the input data.
	error_list = []

	# PATTERNS
	# Limitation: UNICODE not currently supported by this pattern list as the sorting becomes less intuitive.
	# An alternative would be to install PyICU (IBM's ICU Library), to help collate unicode algorithmically.

	# Pattern to be used for first name and full name matches.
	pattern1 = re.compile("(?P<elem>^[a-zA-Z-'\. ]+$)")
	# Pattern to be used with last name matches.
	pattern2 = re.compile("(?P<elem>^[a-zA-Z-']+$)")
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
			name_match = pattern1.match(line_components[0])
			color_match = pattern3.match(line_components[1])
			zip_match = pattern4.match(line_components[2])
			phone_match = pattern6.match(line_components[3])

			success = encapsulate(None, None, name_match, color_match, zip_match, phone_match)

			# If match is found, then capture match and split into first and last name.
			if success:
				lastname = success[2]
				firstname = success[1]
				color = success[0]
				phone = success[3]
				zipcode = success[4]
				# Dictionary entry is to be sorted by (lastname, firstname). Phone number is added
				# as part of the key as well to prevent duplicate entries by the same person.
				if dictionary.get(lastname + firstname + " " + phone.replace("-", "")):
					error_list.append(linecount)
					linecount += 1
					continue
				dictionary[lastname + firstname + " " + phone.replace("-", "")] = \
					collections.OrderedDict([('color', color), ('firstname', firstname), \
					('lastname', lastname), ('phonenumber', phone), ('zipcode', zipcode)])

			else:
				error_list.append(linecount)

		elif len(line_components) == 5:
			# Check format numbers 1, 3.
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
			
			success = None

			# Check format number 1.
			success1 = encapsulate(first_name_match1, last_name_match1, None, color_match1, zip_match1, phone_match1);
			# Check format number 3.
			success2 = encapsulate(first_name_match2, last_name_match2, None, color_match2, zip_match2, phone_match2);

			# Attempt to "DRY" out code to avoid repetition.
			if success1:
				success = success1
			elif success2:
				success = success2

			if success:
				lastname = success[2]
				firstname = success[1]
				color = success[0]
				phone = success[3]
				zipcode = success[4]
				if dictionary.get(lastname + firstname + " " + phone.replace("-", "")):
					error_list.append(linecount)
					linecount += 1
					continue
				dictionary[lastname + firstname + " " + phone.replace("-", "")] = \
					collections.OrderedDict([('color', color), ('firstname', firstname), \
					('lastname', lastname), ('phonenumber', phone), ('zipcode', zipcode)])
			else:
				error_list.append(linecount)

		else:
			# Add to line to errors list (number of arguments do not match).
			error_list.append(linecount)

		linecount += 1
	
	# Sort entries alphabetically and append to entries list.
	for key in sorted(dictionary):
		entries_list.append(dictionary[key])

	# Generate JSON data in dictionary format.
	response = {'entries': entries_list, 'errors': error_list}
	
	# Write JSON data to file, result.out.
	with open('result.out', 'w') as outfile:
		json.dump(response, outfile, sort_keys = True, indent = 2)

	return None