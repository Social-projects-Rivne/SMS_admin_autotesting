import os
basedir = os.path.abspath(os.path.dirname(__file__))

# database credentials
import sys

DB_ROOT = os.path.join(basedir, '..', 'database_settings')
sys.path.append(DB_ROOT)

from db import credentials, USERNAME, PASSWORD

# flask configuration

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)