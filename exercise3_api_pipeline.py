import dlt
import requests
from pathlib import Path
import os
import datetime

# read secrets from .env file
weather_api_key = os.getenv("WEATHER_API_KEY")

# --- create dlt resource --- #
@dlt.resource(write_disposition="append")
def fetch_weather(cities):
    """Generator function to fetch weather data for multiple cities"""
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            # yield one dictionary with parts of data, instead of yielding the entire raw json data
            data = response.json()
            timestamp = datetime.datetime.now().strftime("%Y/%-m/%-d, %H:%M:%S")
            yield {"city": data.get("name"),
                   "timestamp": timestamp,
                   "temperature": data["main"].get("temp"),
                   "humidity": data["main"].get("humidity"),
                   "pressure": data["main"].get("pressure"),
                   "weather_description": data["weather"][0].get("description"),
                   "cloudiness": data["clouds"].get("all")
                   }
        else: 
            yield f"Failed to fetch data for {city}"

# --- create a pipeline object & run the pipeline --- #
def run_pipeline(cities, table_name):
    # create a pipeline object
    db_path = working_directory / "weather.duckdb"
    pipeline = dlt.pipeline(pipeline_name='weather',
                            destination=dlt.destinations.duckdb(str(db_path)),
                            dataset_name="staging"
    )

    # run the pipeline
    # also print out loading information when dlt is running
    load_info = pipeline.run(fetch_weather(cities), table_name=table_name)
    print(load_info)

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    cities = ["London", "New York", "Tokyo"]
    table_name = "current_weather"
    run_pipeline(cities, table_name)

