import pandas as pd
import glob
import os

def read_csv(file_path):
    """Read CSV file with traffic info:
    https://www.gipuzkoairekia.eus/es/datu-irekien-katalogoa
    """
    
    # Columns to be read
    columnas = ["Estacion", "Fecha"]
    carriles = ["Carril 1 ligeros ", "Carril 1 pesados",
                "Carril 4 ligeros ", "Carril 4 pesados"]
    # Measurement point number
    aforo = 9259

    df = pd.read_csv(file_path, sep=";",
                     parse_dates=["Fecha"], dayfirst=True,
                     usecols=(columnas + carriles)
                    )

    df = df.loc[df["Estacion"] == aforo, :]

    df["volume"] = df[carriles].sum(axis=1)
    df.drop(["Estacion"] + carriles, axis=1, inplace=True)

    return df.groupby("Fecha").sum()


# Path to folder with CSV files
folder_path = "../csvs/datosvolumen"

# Get list of all CSV files in the folder
files = glob.glob(os.path.join(folder_path, "*.csv"))

# Read files
dfs = []
for file in files:
    dfs.append(read_csv(file))

# Concatenate dataframes
df = pd.concat(dfs)

# Save to file
file_name = "trafikoa"
df.to_csv(f"../data/{file_name}.csv")