from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

SQLITE = 'sqlite'
PLAYERS = 'players'

class MyDatabase:
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

    def test_insert(self):
        query = "INSERT INTO 'players'(id, number, name, nationality, position, birthday, height, join_date, contract, price) "\
                "VALUES (0, 5, 'Ryan Parel', 'United States', 'Defender', '10-03-98', '5-11', '9-05-2019', '9-05-2020', '$50.00m');"
        self.execute_query(query)
        self.print_all_data(PLAYERS)

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

    def execute_query(self, query=''):
        if query == '': return
        print(query)

        with self.db_engine.connect() as connection:
            try:
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

def main():
    dbms = MyDatabase(SQLITE, dbname="testdb.sqlite")
    dbms.create_db_tables()
    dbms.test_insert()
    dbms.print_all_data(PLAYERS)

if __name__ == "__main__":
    main()