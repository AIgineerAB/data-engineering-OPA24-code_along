import dlt
import requests
from pathlib import Path
import os

#--- create dlt.source object ---#

# define a generator function
def get_resource(url, endpoint):
    yield requests.get(url + "/" + endpoint).json()

# using the generator function to create a dlt.source object
# under this dlt.source object, we can have several dlt.resource objects
@dlt.source
def hubspot():

    url = 'https://jobsearch.api.jobtechdev.se'
    endpoints = ["search", "complete"]

    for endpoint in endpoints:
        yield dlt.resource(get_resource(url, endpoint), 
                           name=endpoint,
                           write_disposition="replace")
        
# create a pipeline object and function to run the pipeline
def run_pipeline_source():

    pipeline_source = dlt.pipeline(pipeline_name="jobsearch_source",
                                   destination=dlt.destinations.duckdb(f"{working_directory}/ads_source.duckdb"),
                                   dataset_name="staging")
    
    source = hubspot()

    load_info_source = pipeline_source.run(source.with_resources("search", "complete"))
    print(load_info_source)

if __name__=="__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline_source()