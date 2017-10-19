import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://testuser:testpassword@localhost/OASdb'
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'something very secretive and no one knows it!!'

# MYSQL_DATABASE_USER = 'testuser'
# MYSQL_DATABASE_PASSWORD = 'testpassword'
# MYSQL_DATABASE_DB = 'phpdb'
# MYSQL_DATABASE_HOST = 'localhost'