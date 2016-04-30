cd ../
python -m unittests.test_schools_model_with_entity
coverage run -m unittests.test_schools_model_with_entity
coverage report -m unittests/test_schools_model_with_entity.py
coverage html unittests/test_schools_model_with_entity.py

