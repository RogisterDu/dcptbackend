class Config:
    HOST = '8.210.51.91'
    PORT = '3306'
    DATABASE = 'dcpt'
    USERNAME = 'dcpt'
    PASSWORD = 'Rt192197'

    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4"\
        .format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    SCHEDULER_API_ENABLED = True
