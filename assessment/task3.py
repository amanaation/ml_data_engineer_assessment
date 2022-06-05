from sqlalchemy import create_engine, Table, MetaData
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
                    level=logging.NOTSET)
logger = logging.getLogger(__name__)


class DB:
    file_type_function_mapping = {
        'csv': pd.read_csv,
        'json': pd.read_json,
    }

    def __init__(self, db_host: str,
                 db_port: int,
                 db_user: str,
                 db_password: str,
                 database: str,
                 engine='mysql') -> None:
        self.engine = create_engine(f'{engine}://{db_user}:{db_password}@{db_host}:{db_port}/{database}')

    def bulk_transfer_from_file(self, file_path,
                                file_type: str,
                                target_table: str,
                                if_exists='replace') -> None:
        try:
            file_type = file_type.lower()
            reader = self.file_type_function_mapping[file_type]
            df = reader(file_path)
            with self.engine.connect() as connection:
                df.to_sql(target_table, connection, if_exists=if_exists, index=False)
            logger.info(f"{file_type.upper()} to SQL transfer success!!")
        except Exception as e:
            logger.error("Following occurred while transferring data from csv to sql :")
            logger.error(e)

    def single_record_transfer(self, table: str, record: dict):
        meta = MetaData()
        table_obj = Table(table, meta, autoload=True, autoload_with=self.engine)
        insert_query = table_obj.insert().values(**record)
        self.execute_query(insert_query)

    def execute_query(self, query):
        with self.engine.connect() as connection:
            logger.info("Connection to Database Successful")
            logger.info(f"Executing query {query}")
            response = connection.execute(query)
            if not response._soft_closed:
                return response.fetchall()


if __name__ == "__main__":
    connection_details = {"database": "datatestdb",
                          "db_user": "datatest",
                          "db_password": "alligator",
                          "db_host": "127.0.0.1",
                          "db_port": 3300,

                          }
    db = DB(**connection_details)
    db.bulk_transfer_from_file(target_table='people',
                               file_path='data/people.csv',
                               file_type='csv')
    db.single_record_transfer('people', {"Name": "Dr.Flintsone"})
    print(db.execute_query("insert into people(name, age) values('Albert Einstien', 60)"))
