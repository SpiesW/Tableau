import pandas as pd

# Read in unemployment data and drop excess columns
# Note this script is set up to run with csv files in the same directory
unemp = pd.read_csv("unemployment.csv")
unemp = unemp.drop(columns=["Series Name", "Series Code", "Country Name", "Country Code"])

# Clean unemployment data and save in new csv for easy viewing
# Here we only get years 1960-2022 inclusive and unemployment rate for each
new_unemp = pd.DataFrame()
years = [x for x in range(1960, 2023)]
new_unemp['Year'] = years
new_unemp['Unemployment Rate'] = list(unemp.iloc[0])

# Write data out for easy viewing
new_unemp.to_csv("cleaned_unemployment.csv", index=False)

# Read in president data
pres = pd.read_csv("us_presidents.csv")
pres = pres[['start', 'end', 'president', 'party']]

# Fill in missing end date for Trump
pres.loc[44, "end"] = "20-Jan-21"

# Select only rows for presidents we have corresponding unemployment data for
pres = pres.loc[33:,]
pres = pres.reset_index(drop=True)

# Map start/end columns to have last 2 digits of the year
pres["start"] = pres["start"].map(lambda x: x[-2:])
pres["end"] = pres["end"].map(lambda x: x[-2:])

# Prepend 19/20 to years
year_front_start = ["19" for _ in range(9)] + ["20" for _ in range(3)]
year_front_end = ["19" for _ in range(8)] + ["20" for _ in range(4)]

# Subtract 1 from each end year so president start/ends do not overlap
for i in range(len(pres["start"])):
    pres.loc[i, "start"] = int(year_front_start[i] + pres.loc[i, "start"])
    pres.loc[i, "end"] = int(year_front_end[i] + pres.loc[i, "end"]) - 1

# Function to get the corresponding president for a year in the unemployment data
def lambda_func1(x):
    for row in pres.iterrows():
        if x >= row[1]["start"] and x <= row[1]["end"]:
            return row[1]["president"]
    return "Not In Dataset"

# Function to get the corresponding party for a year in the unemployment data
def lambda_func2(x):
    for row in pres.iterrows():
        if x >= row[1]["start"] and x <= row[1]["end"]:
            return row[1]["party"]
    return "Not In Dataset"

# Map data
new_unemp['President'] = new_unemp['Year'].map(lambda_func1)
new_unemp['Party'] = new_unemp['Year'].map(lambda_func2)


# Write final data to csv for Tableau
new_unemp.to_csv("Dataset.csv", index=False)
