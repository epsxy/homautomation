from rethinkdb import r


class ReDB:
    host: str = None
    port: int = None
    conn = None

    def __init__(self, host: str ='localhost', port: int = 28015):
        self.host = host
        self.port = port

    def connect(self):
        self.conn = r.connect(self.host, self.port).repl()
        tables = r.db('dashboard').table_list().run(self.conn)
        print('tables list: {}'.format(tables))
        if ('temperatures' not in tables):
            print('creating temperatures table')
            r.db('dashboard').table_create('temperatures').run(self.conn)
        if ('humidity' not in tables):
            print('creating humidity table')
            r.db('dashboard').table_create('humidity').run(self.conn)

    def get_conn(self):
        return self.conn
