class Config:
    SECRET_KEY = 'jlkjksfksdfsdsdkfkfjsksfsk' 
    SQLALCHEMY_DATABASE_URI = 'postgres://agelflaf:K_qq9qjFitZIsOMQF_sUShyQMmEeyVS9@lallah.db.elephantsql.com:5432/agelflaf' #move to env in prod
    MAX_ROUNDS = 2
    
class DevelopmentConfig(Config):
    DEBUG = True 

class ProductionConfig(Config):
    DEBUG = False 
