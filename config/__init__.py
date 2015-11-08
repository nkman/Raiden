import os, json

def twitter_credentials():
    DB_PATH = os.path.join(os.path.dirname(__file__), 'twitter.json')
    config_file = os.path.abspath(DB_PATH)
    
    with open(config_file, 'r') as f:
        config = f.read()
        f.close()

    config = json.loads(config)
    return config

def db_credentials():

    DB_PATH = os.path.join(os.path.dirname(__file__), 'database.json')
    config_file = os.path.abspath(DB_PATH)
    
    with open(config_file, 'r') as f:
        config = f.read()
        f.close()

    config = json.loads(config)
    return config
