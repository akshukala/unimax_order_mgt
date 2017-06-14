from datetime import timedelta


class BaseConfig(object):
    SITE_URL = 'http://localhost/'
    DEBUG = True
    REQUEST_RETRY = 3
    PERMANENT_SESSION_LIFETIME = timedelta(365)
    CORS_ALLOW_HEADERS = ['Origin', 'Content-Type',
                          'Accept', 'X-Authorization-Token']
    CORS_ALLOW_ORIGINS = ['*']
    CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    AGRO_HOST = 'localhost:8000'
    AGRO_HTTPS = False
