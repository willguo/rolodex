import unittest
import rolodex

# *** UNICODE PROPERTIES ARE NOT SUPPORTED IN PYTHON WITHOUT USE OF EXTERNAL LIBRARIES. ***

class TestRolodexMethods(unittest.TestCase):

  # Sample test (given in specs).
  def test_given(self):
    output = None
    expected = None
    rolodex.normalize("test/test1.in")
    with open ("result.out", "r") as outputfile:
      output = outputfile.read()
    with open ("test/test1.out", "r") as expectedfile:
      expected = expectedfile.read()
    self.assertTrue(output)
    self.assertTrue(expected)
    self.assertEqual(output, expected)
  
  # Test to check precedence of alphabetical ordering (by lastname, then firstname).
  def test_alpha_precedence(self):
    output = None
    expected = None
    rolodex.normalize("test/test2.in")
    with open ("result.out", "r") as outputfile:
      output = outputfile.read()
    with open ("test/test2.out", "r") as expectedfile:
      expected = expectedfile.read()
    self.assertTrue(output)
    self.assertTrue(expected)
    self.assertEqual(output, expected)

  # Test empty input.
  def test_empty(self):
    output = None
    expected = None
    rolodex.normalize("test/test3.in")
    with open ("result.out", "r") as outputfile:
      output = outputfile.read()
    with open ("test/test3.out", "r") as expectedfile:
      expected = expectedfile.read()
    self.assertTrue(output)
    self.assertTrue(expected)
    self.assertEqual(output, expected)

  # Test irregular input, including duplicate entries/entries by the same person (tracked by phone number)
  # as well as names that contain dashes and apostrophes. Duplicate entries or entries posted by a person 
  # with an already existing phone number filed will be reported as errors.
  def test_duplicates(self):
    output = None
    expected = None
    rolodex.normalize("test/test4.in")
    with open ("result.out", "r") as outputfile:
      output = outputfile.read()
    with open ("test/test4.out", "r") as expectedfile:
      expected = expectedfile.read()
    self.assertTrue(output)
    self.assertTrue(expected)
    self.assertEqual(output, expected)

  # Test for data.in file (target problem).
  def test_provided_data(self):
    output = None
    expected = None
    rolodex.normalize("data.in")
    with open ("result.out", "r") as outputfile:
      output = outputfile.read()
    with open ("test/test_final.out", "r") as expectedfile:
      expected = expectedfile.read()
    self.assertTrue(output)
    self.assertTrue(expected)
    self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()