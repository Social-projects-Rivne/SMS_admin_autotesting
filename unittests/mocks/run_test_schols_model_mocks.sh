cd ../../
python -m unittests.mocks.test_schools_model_with_entity_mocks
coverage run -m unittests.mocks.test_schools_model_with_entity_mocks
coverage report -m unittests/mocks/test_schools_model_with_entity_mocks.py
coverage html unittests/mocks/test_schools_model_with_entity_mocks.py
