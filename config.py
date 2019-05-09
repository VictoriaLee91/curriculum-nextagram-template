import os

S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'
AWS_LINK = f'http://s3-ap-southeast-1.amazonaws.com/{S3_BUCKET}'
MERCHANT_ID = os.environ.get("SANDBOX_MERCHANT_ID"),
PUBLIC_KEY = os.environ.get("SANDBOX_PUBLIC_KEY"),
PRIVATE_KEY = os.environ.ger("SANDBOX_PRIVATE_KEY")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
