cd ../../
python -m unittests.mocks.test_roles_model_with_entity_mocks
coverage run -m unittests.mocks.test_roles_model_with_entity_mocks
coverage report -m unittests/mocks/test_roles_model_with_entity_mocks.py
coverage html unittests/mocks/test_roles_model_with_entity_mocks.py
firefox htmlcov/app_models_roles_model_with_entity_py.html
