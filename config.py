import os 

class Config:
    #Secret key is used by flask to protect session data and forms from hinderance
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_scret_key'

    #Database config: using sqLite file stored in 'instance/hospital.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'

    #disable modeification tracking (save resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False