import re


class Validate(object):

    """This class check on request data from form by pattern"""

    # regex pattern
    email_pattern = "^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}$"
    name_pattern = "^([A-Z\p{Cyrillic}])\w\p{Cyrillic}+\s([A-Z{Cyrillic}])\w\p{Cyrillic}+$"
    login_pattern = "^[A-Za-z0-9]+$"

    def __init__(self):
        pass

    def check_email(self, input_str):
        """check email"""

        return re.match(self.email_pattern, input_str)

    def check_name(self, input_str):
        """check name"""

        return re.match(self.name_pattern, input_str)

    def check_login(self, input_str):
        """check login"""

        return re.match(self.login_pattern, input_str)
