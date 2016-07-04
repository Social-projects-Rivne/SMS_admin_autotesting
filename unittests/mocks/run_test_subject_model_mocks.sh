cd ../..
python -m unittests.mocks.test_subjects_model_with_entity_mocks

coverage run -m unittests.mocks.test_subjects_model_with_entity_mocks
coverage report -m unittests/mocks/test_subjects_model_with_entity_mocks.py
pylint unittests/mocks/test_subjects_model_with_entity_mocks.py
read -n1 -r -p 'Press any key to open html report...' key
coverage html unittests/mocks/test_subjects_model_with_entity_mocks.py
firefox htmlcov/unittests_mocks_test_subjects_model_with_entity_mocks_py.html
