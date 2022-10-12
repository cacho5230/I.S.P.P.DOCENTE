
class Config:
    SECRET_KEY = 'SAD34254GF45'

class connDb(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'ispp_docentes'
    MYSQL_PORT = 3309

config = {
    'desarrollo' : connDb
}