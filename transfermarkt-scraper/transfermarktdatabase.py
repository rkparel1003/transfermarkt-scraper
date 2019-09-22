from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

SQLITE = 'sqlite'
PLAYERS = 'players'


class TransfermarktDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname = ''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metaData = MetaData()
        players = Table(PLAYERS, metaData,
                        Column('id', Integer, primary_key=True),
                        Column('team_name', String),
                        Column('number', Integer),
                        Column('name', String),
                        Column('nationality', String),
                        Column('position', String),
                        Column('birthday', String),
                        Column('height', String),
                        Column('join_date', String),
                        Column('contract', String),
                        Column('price', String)
        )
        try:
            metaData.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occured during Table creation!")
            print(e)

    def execute_query(self, values=None, query=''):
        if query == '': return
        print(query)

        with self.db_engine.connect() as connection:
            try:
                if values:
                    connection.execute(query, values)
                else:
                    connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)  # print(row[0], row[1], row[2])
                result.close()
                print("\n")
