cd ../
python -m unittests.test_view
coverage run -m unittests.test_view
coverage report -m unittests/test_view.py
coverage html unittests/test_view.py

python -m unittests.test_login_required
coverage run -m unittests.test_login_required
coverage report -m unittests/test_login_required.py
coverage html unittests/test_login_required.py

