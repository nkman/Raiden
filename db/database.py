import rethinkdb as r
import config

class Database:

    def __init__(self):
        
        configuration = config.db_credentials()
        self.host = configuration['host']
        self.port = configuration['port']
        self.db = configuration['db']
        self.auth_key = configuration['auth_key']
        self.initiate_connection()

    def initiate_connection(self):

        self.connection = r.connect(host=self.host,
            port=self.port,
            db=self.db,
            auth_key=self.auth_key
        )

    def restart_connection(self):
        self.connection.close()
        initiate_connection()

    def connection_var(self):
        return self.connection
