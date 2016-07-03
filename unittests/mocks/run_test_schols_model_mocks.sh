#/bin/bash
#cd ../../
python -m unittests.mocks.test_schools_model_with_entity_mocks
read -n1 -r -p 'Press any key...' key 
coverage run -m unittests.mocks.test_schools_model_with_entity_mocks
coverage report -m unittests/mocks/test_schools_model_with_entity_mocks.py
read -n1 -r -p 'Press any key...' key 
coverage html unittests/mocks/test_schools_model_with_entity_mocks.py
firefox htmlcov/app_models_schools_model_with_entity_py.html 