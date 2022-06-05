from task3 import DB


class Analytics:

    def __init__(self):
        connection_details = {"database": "datatestdb",
                              "db_user": "datatest",
                              "db_password": "alligator",
                              "db_host": "127.0.0.1",
                              "db_port": 3300,

                              }

        self.TABLE = 'people'
        self.db = DB(**connection_details)

    def get_minimum(self, column):
        try:
            query = f"select min({column}) as min_{column} from {self.TABLE}"
            result = self.db.execute_query(query)
            return result[0][0]
        except Exception as e:
            return e

    def get_maximum(self, column):
        try:
            query = f"select max({column}) as max_{column} from {self.TABLE}"
            result = self.db.execute_query(query)
            return result[0][0]
        except Exception as e:
            return e

    def get_average(self, column):
        try:
            query = f"select avg({column}) as avg_{column} from {self.TABLE}"
            result = self.db.execute_query(query)
            return result[0][0]
        except Exception as e:
            return e

    def get_city_with_most_people(self):
        try:
            query = f"select city from {self.TABLE} group by City  order by count(*) DESC limit 1"
            result = self.db.execute_query(query)
            return result[0][0]
        except Exception as e:
            return e

    def get_top_5_interests(self):
        try:
            query = f"""select interest1 as interest, count(*) as occurence from (
                            select Interest1  from {self.TABLE} p where Interest1 is not null 
                            union all  
                            select Interest2  from {self.TABLE} p2  where Interest2 is not null
                            union all  
                            select Interest3  from {self.TABLE} p3  where Interest3 is not null
                            union all  
                            select Interest4  from {self.TABLE} p4  where Interest4 is not null		
                    ) as p3 group by Interest1 order by occurence desc limit 5;        
            """

            result = self.db.execute_query(query)
            return result
        except Exception as e:
            return e


if __name__ == "__main__":
    an = Analytics()
    print("Maximum age : ", an.get_maximum('age'))
    print("Minimum age : ", an.get_minimum('age'))
    print("Average age : ", an.get_average('age'))
    print("City with most people : ", an.get_city_with_most_people())
    print("Top 5 interests : ", an.get_top_5_interests())
