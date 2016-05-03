#/bin/bash
#cd ../
python -m unittests.test_schools_model_with_entity
read -n1 -r -p 'Press any key...' key 
coverage run -m unittests.test_schools_model_with_entity
coverage report -m unittests/test_schools_model_with_entity.py
read -n1 -r -p 'Press any key...' key 
coverage html unittests/test_schools_model_with_entity.py
firefox htmlcov/app_models_schools_model_with_entity_py.html 
