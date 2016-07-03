cd ..
cd ..
python -m unittests.mocks.test_roles_model_mocks
coverage run -m unittests.mocks.test_roles_model_mocks
coverage report -m unittests/mocks/test_roles_model_mocks.py 
coverage html unittests/mocks/test_roles_model_mocks.py
pylint unittests.mocks.test_roles_model_mocks 

