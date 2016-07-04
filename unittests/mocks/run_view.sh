cd ..
cd ..
python -m unittests.mocks.test_view_mocks
coverage run -m unittests.mocks.test_view_mocks
coverage report -m unittests/mocks/test_view_mocks.py 
coverage html unittests/mocks/test_view_mocks.py
pylint unittests.mocks.test_view_mocks 

