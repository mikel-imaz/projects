import pandas as pd

# Define function
def read_calendar(file_path):
    """Read CSV file with calendar info:
    https://opendata.euskadi.eus/catalogo
    """

    df = pd.read_csv(file_path, sep=";",
                     usecols=["date", "descripcionEs", "municipalityEs"],
                     parse_dates=["date"], dayfirst=True, date_format="ISO8601",
                     index_col="date",
                    )

    return df.loc[df["municipalityEs"].str.strip().isin(["CAE", "Gipuzkoa"]), :]


# Define file names
year_first = 2021
year_last = 2025
files = [f"calendario_laboral_202{x}.csv" for x in range(year_first % 2020, (year_last + 1) % 2020)]

# Read files
path = "../csvs/calendarios/"
dfs = []
for file in files:
    dfs.append(read_calendar(path + file))

# Concatenate dataframes
df = pd.concat(dfs)

# Just "holiday" column
df["holiday"] = 1
df.drop(["descripcionEs", "municipalityEs"], axis=1, inplace=True)

# Save to file
file_name = "festak"
df.to_csv(f"../data/{file_name}.csv")