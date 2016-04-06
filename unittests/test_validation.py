import unittest

from app.utils.validation import Validate

class TestValidation(unittest.TestCase):
	
	def test_creation_of_validator(self):
		""" Creation of object typeof Validate """
		validator = Validate()
		self.assertIsInstance(validator, Validate)
	
	validator = Validate()	
	def test_check_email_correct(self):
		""" Check if correct email matched """
		str_to_test = "alex@gmail.com"
		result = validator.check_email(str_to_test)
		self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main(verbosity=2)