from datetime import timedelta


class Config:
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"

    # Flask-Session
    SESSION_TYPE = "sqlalchemy"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    GOOGLE_OAUTH_CLIENT_ID = "854325940723-clpnbi3kjqm1khs759hb1lt7ls8ve84g.apps.googleusercontent.com"
    GOOGLE_SERVER_METADATA_URL = "https://accounts.google.com/.well-known/openid-configuration"

class LocalConfig(Config):
    NAME = "local"

    TESTING = True

class FlyConfig(Config):
    pass
