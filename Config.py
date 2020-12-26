import os


class BaseConfig:
    ROOT_DIR = os.getcwd()
   
    
    #####MYSQL
    MYSQL_HOST = 'sot-axsfelzaxfnpzn.cwejgvog2er4.ap-southeast-1.rds.amazonaws.com'
    MYSQL_USER = 'master_admin'
    MYSQL_PASSWORD = 'kQwpGRtXiunCRzfelz'
    MYSQL_DB = 'wound'


    #####S3_BUCKET    
    S3_BUCKET = "dev.trails.wound.management" 

    

class DevConfig(BaseConfig):
    CONFIG_NAME = 'Dev'

class BulkUploadConfig(BaseConfig):
    CONFIG_NAME = 'BulkUpload'
   

class ProdConfig(BaseConfig):
    CONFIG_NAME ='Prod'
    
class RunTimeConfig(BaseConfig):
    CONFIG_NAME = 'RunTimeConfig'
    