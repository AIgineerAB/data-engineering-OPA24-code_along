import pandas as pd
from pathlib import Path #we import a class called Path from library pathlib

def read_data():
    data_path = Path(__file__).parents[1]/"data"
    df = pd.read_excel(data_path/"resultat-ansokningsomgang-2024.xlsx", skiprows=5, sheet_name="Tabell 3")
    return df

if __name__ == "__main__":
    #testing purpose
    df = read_data()
    print(df.columns)
