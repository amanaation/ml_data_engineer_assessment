from sqlalchemy import create_engine, Table, MetaData
import pandas as pd
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
                    level=logging.NOTSET)
logger = logging.getLogger(__name__)


class DB:
    def _intialize_connection(self, db_host: str,
                              db_port: int,
                              db_user: str,
                              db_password: str,
                              database: str,
                              engine='mysql') -> None:
        self.engine = create_engine(f'{engine}://{db_user}:{db_password}@{db_host}:{db_port}/{database}')

    def bulk_transfer_from_csv(self, table: str,
                               data_file_path: str,
                               if_exists='replace') -> None:
        try:
            df = pd.read_csv(data_file_path)
            with self.engine.connect() as connection:
                df.to_sql(table, connection, if_exists=if_exists, index=False)
            logger.info("CSV to SQL transfer success!!")
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
    db = DB()
    db._intialize_connection(**connection_details)
    # db.bulk_transfer_from_csv('people3',
    #                           '/Users/amanmishra/Desktop/aman/asessment/ml_data_engineer_assessment/data/people3.csv')
    # db.single_record_transfer('people2', {"Name": "Aman Mishra"})
    print(db.execute_query("insert into people2(name) values('Aman Mishra')"))
