
# Include private.py in this directory for passwords and other secret stuff.
try:
    from . import private
    BasePrivate = private.PrivateConfig
except ImportError as e:
    BasePrivate = object


class BaseConfig(BasePrivate):
    HOST = '0.0.0.0'
    PORT = 5000
    ENCODERS_PATH = 'config/encoders.pkl'
    MODEL_PATH = 'config/model.pkl'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

