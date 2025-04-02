import dlt 
import pandas as pd
from pathlib import Path 
import os #during execution of python script, changing working directory


# --- explanation of dlt.resource object --- #
# dlt uses dlt.source vs dlt.resource for keeping a structure of data sources 
# example: one api vs different endpoints 
# example: one excel vs different sheets 
# for current data, we have one csv file, so we can create dlt.resource directly


# --- explanation of how to create a dlt.resource object --- #
# to create a dlt.resource object as a raw data source
# how to define
# - create a function to read csv file with pandas -> output is a function and this function yield a df object
# - use the dlt.resource decorator to produce a dlt.resource object -> output is a dlt.resource object because the dlt.resource decorator is modifying your input function 


# --- code for create a dlt.resource object ---#
@dlt.resource(write_disposition="replace")
def load_csv_resource(file_path: str, **kwargs): 
    df = pd.read_csv(file_path, **kwargs)
    yield df #yield keyword is a lazy evaluation compared to return keyword


if __name__ == "__main__":

    # --- set up data file path --- #
    working_directory = Path(__file__).parent
    csv_path = working_directory / "data" / "NetflixOriginals.csv"
    data = load_csv_resource(csv_path, encoding = "latin1")
    # checking object type to see that the dlt.resource decorator works 
    #print(type(data))

    # --- create a dlt.pipeline oject --- #
    pipeline = dlt.pipeline(pipeline_name="movies", 
                            destination=dlt.destinations.duckdb(f"{working_directory}" + "/data/movies.duckdb"), #data warehouse info
                            dataset_name="staging",#schema name in the created db
                            )
    
    load_info = pipeline.run(data, table_name="netflix")
    print(load_info)