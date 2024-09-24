from datetime import timedelta


class Config:
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"

    # Flask-Session
    SESSION_TYPE = "sqlalchemy"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
