import dlt
import requests
from pathlib import Path #find a directory
import os #change working directory when running .py

# --- create dlt.resource object --- #

# step 1 - create a function to be used in the generator function
def get_ads(url_for_search, params):
    response = requests.get(url_for_search, params=params)
    return response.json()

# step 3 - use the dlt.resource decorator to produce a dlt.resource object
@dlt.resource(write_disposition="replace")
# step 2 - define the generator function with yield keyword, to be decorated by dlt.resource decorator
def jobsearch_resource(params):

    url = 'https://jobsearch.api.jobtechdev.se'
    url_for_search = f"{url}/search"

    for ad in get_ads(url_for_search, params)["hits"]:
        yield ad

# --- create a pipeline object and a function to run the pipeline object --- #

def run_pipeline(query, table_name): 
    pipeline = dlt.pipeline(pipeline_name='jobsearch',
                            destination=dlt.destinations.duckdb(f"{working_directory}/ads_resource.duckdb"),
                            dataset_name='staging'
                            )
    
    params = {"q":query, "limit":100}
    load_info = pipeline.run(jobsearch_resource(params=params), table_name=table_name)
    print(load_info)


if __name__=="__main__":
    #confirm the working directory is the one storing the .dlt folder, which is the same as the folder storing the current file
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    #execution for data loading
    query = "data engineer"
    table_name = "data_field_job_ads"
    run_pipeline(query, table_name)


