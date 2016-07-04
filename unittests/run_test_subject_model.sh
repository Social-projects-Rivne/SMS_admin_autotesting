cd ../
python -m unittests.test_subjects_model_with_entity

coverage run -m unittests.test_subjects_model_with_entity
coverage report -m unittests/test_subjects_model_with_entity.py
pylint unittests/test_subjects_model_with_entity.py
read -n1 -r -p 'Press any key to open html report...' key
coverage html unittests/test_subjects_model_with_entity.py
firefox htmlcov/unittests_test_subjects_model_with_entity_py.html
