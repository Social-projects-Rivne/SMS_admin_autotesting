#/bin/bash
#cd ../
python -m unittests.test_controller
read -n1 -r -p 'Press any key...' key 
coverage run -m unittests.test_controller
coverage report -m unittests/test_controller.py
read -n1 -r -p 'Press any key...' key 
coverage html unittests/test_controller.py
firefox htmlcov/app_controllers_controller_py.html
