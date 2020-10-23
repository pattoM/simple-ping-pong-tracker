class Config:
    SECRET_KEY = 'jlkjksfksdfsdsdkfkfjsksfsk' 
    SQLALCHEMY_DATABASE_URI = 'postgres://qjckgznj:owBNo4g_2Dtmdi5hrGYqcP_72kOTzO9R@lallah.db.elephantsql.com:5432/qjckgznj' #move to env in prod
    MAX_ROUNDS = 2
    LIM = 2
    
class DevelopmentConfig(Config):
    DEBUG = True 

class ProductionConfig(Config):
    DEBUG = False 
