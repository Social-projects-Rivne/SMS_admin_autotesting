""" Script to run all integration tests as a module at once """
# -*- coding: utf-8 -*-

import unittest

from unittests.test_controller import TestAdminController, \
    TestAdminController_school, \
    TestAdminController_subject, \
    TestAdminController_teacher
from unittests.test_dbdriver import TestDBDriver
from unittests.test_login_required import TestLoginRequired
from unittests.test_roles_model import TestRolesModel
from unittests.test_roles_model_with_entity import TestExtendedRolesModel, \
    TestExtendedRolesModel
from unittests.test_schools_model_with_entity import TestSchool, \
    TestExtendedSchoolsModel
from unittests.test_subjects_model_with_entity import TestSubject, \
    TestExtendedSubjectsModel
from unittests.test_teacher_model_with_entity import TestTeachers, \
    TestTeachersModelWithEntity
# from unittests.test_validation import TestValidation  #  Broken file
from unittests.test_view import TestView

if __name__ == "__main__":
    unittest.main(verbosity=2)
