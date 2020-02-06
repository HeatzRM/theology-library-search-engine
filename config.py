import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = "ab9af4c976dbb8c664fb205079b0e94d013572ebfd755c13af2b7b95b988b843"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    S3_BUCKET=os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")
