import rethinkdb as r

class Database:

    def __init__(self):

        self.host = config['host']
        self.port = config['port']
        self.db = config['db']
        self.auth_key = config['auth_key']
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
