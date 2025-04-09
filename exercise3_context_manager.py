import duckdb 
from pathlib import Path
import os
import pandas as pd

working_directory = Path(__file__).parent
os.chdir(working_directory)
db_path = working_directory / "weather.duckdb"

# --- without context manager --- #
# conn = duckdb.connect(str(db_path))
# print(conn.execute("SELECT * FROM staging.current_weather").fetchone())
# NEED TO CLOSE THE CONNECTION MANUALLY!

# --- with context manager with duckdb --- #
# with duckdb.connect(str(db_path)) as conn:
#     print(conn.execute("SELECT * FROM staging.current_weather").fetchone())

# --- with own context manager --- #
# a class with __enter__ and __exit__ methods
# --> context manager is implemented
# --> with statement can be used 
# --> equivalent to working with files

# #define a simple class with context manager 
# class Test:
#     def __init__(self):
#         pass
    
#     def __enter__(self):
#         print("entering __enter__")

#     def __exit__(self, exc_type, exc_value, traceback):
#         print("exiting __exit__")

# #execute a code with an object from this class
# with Test() as test: 
#     print("inside of context manager")

# define a class with context manager for database conneciton
class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = duckdb.connect(self.db_path)
        return self 

    def query(self, query):
        return self.connection.execute(query).df()
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

with Database(db_path) as db:
    query1 = db.query("SELECT * FROM staging.current_weather")

    print(type(query1))
    print(query1)