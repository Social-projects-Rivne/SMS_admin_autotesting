""" Script to run all unittests as a module at once """
# -*- coding: utf-8 -*-

import unittest

from unittests.mocks.test_roles_model_mocks import TestRolesModel
from unittests.mocks.test_roles_model_with_entity_mocks import TestRole, \
    TestExtendedRolesModel
from unittests.mocks.test_schools_model_with_entity_mocks import TestSchool, \
    TestExtendedSchoolsModel
from unittests.mocks.test_subjects_model_with_entity_mocks import TestSubject, \
    TestExtendedSubjectsModel
from unittests.mocks.test_teacher_model_with_entity_mocks import TestTeachers, \
    TestTeachersModelWithEntity

if __name__ == "__main__":
    unittest.main(verbosity=2)
