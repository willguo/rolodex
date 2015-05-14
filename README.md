Author: William Guo

Coding Challenge (Percolate): Creating back end functionality of rolodex.

OVERVIEW:
=========
This program takes in n lines of input, each with entry information, and writes a valid, formatted
JSON object out to result.out. Entries are ordered in alphabetical order by (Last Name, First Name).
This problem is described in greater detail in /specifications/rolodex_instructions.pdf.

Additionally, they are sorted by phone number as a means to remove duplicate entries by the same person.
Lines with entries corresponding to an already existing user (same first name, last name, and phone number)
will be marked as "errors" and appended to the errors list. This was not detailed in the specifications;
however, it made logical sense for me to filter out duplicate/spam entries.

Unicode characters are currently not supported by this implementation (sorting more intuitively would require
a better-suited library); however, this is definitely a feature I would like to look into given more time.

TESTING:
========
All tests and test output files can be found in the /test directory.

The unit tests can be run in the terminal by the following command: 

$ python rolodex_test.py"

You may also choose to test your own input manually via the terminal. To do this, simply run the following
command, where "input.in" specifies the name of your input file:

$ python -c 'from rolodex import *; normalize("input.in")'

The result should be written to the result.out file located in the project directory.
