cd ../
python -m unittests.test_roles_model_with_entity
coverage run -m unittests.test_roles_model_with_entity
coverage report -m unittests/test_roles_model_with_entity.py
coverage html unittests/test_roles_model_with_entity.py

