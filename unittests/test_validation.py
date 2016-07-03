import unittest

from app.utils.validation import Validate


class TestValidation(unittest.TestCase):
    """ Class to test Validate class """
    def setUp(self):
        """ Preparation """
        self.validator = Validate()

    def test_check_email_positive(self):
        """ Check whether correct email matched """
        str_to_test = "alexv@gmail.com"
        result = self.validator.check_email(str_to_test)
        self.assertIsInstance(result, object)

    def test_check_email_negative(self):
        """ Check whether wrong email matched """
        str_to_test = u"alexgmail.com"
        result = self.validator.check_email(str_to_test)
        self.assertIsNone(result)

    def test_check_cyrrilic_negative(self):
        """ Check whether matched non-cyrillic text for cyrillik pattern """
        str_to_test = "sdaskfnsajkfnas"
        result = self.validator.check_cyrillic(str_to_test)
        self.assertIsNone(result)

    def test_check_cyrrilic_positive(self):
        """ Check whether matched cyrillic text for cyrillik pattern """
        str_to_test = u"Кирилиця для тесту№1Є"
        result = self.validator.check_cyrillic(str_to_test)
        self.assertIsInstance(result, object)

    def test_check_name_positive(self):
        """ Check whether matched correct name """
        str_to_test = u"Красавчік Kewa Аполонович"
        result = self.validator.check_name(str_to_test)
        self.assertIsInstance(result, object)

    def test_check_name_negative(self):
        """ Check whether matched non correct name """
        str_to_test = u"Зюганов Genadii 000"
        result = self.validator.check_name(str_to_test)
        self.assertIsNone(result)

    def test_check_login_positive(self):
        """ Check whether matched correct login """
        str_to_test = "nagibator2000"
        result = self.validator.check_login(str_to_test)
        self.assertIsInstance(result, object)

    def test_check_login_negative(self):
        """ Check whether matched non correct login """
        str_to_test = "dsad?+-12"
        result = self.validator.check_login(str_to_test)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

