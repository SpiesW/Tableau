import pandas as pd
from datetime import date

unemp = pd.read_csv("unemployment.csv")
unemp = unemp.drop(columns=["Series Name", "Series Code", "Country Name", "Country Code"])

# print(type(unemp.iloc[0]))

new_unemp = pd.DataFrame()
years = [x for x in range(1960, 2023)]
# print(years)
new_unemp['Year'] = years
new_unemp['Unemployment Rate'] = list(unemp.iloc[0])
# print(new_unemp.head())

# new_unemp.to_csv("cleaned_unemployment.csv", index=False)

pres = pd.read_csv("us_presidents.csv")
pres = pres[['start', 'end', 'president', 'party']]
pres.loc[44, "end"] = "20-Jan-21"
pres = pres.loc[33:,]
pres = pres.reset_index(drop=True)
# print(pres)
pres["start"] = pres["start"].map(lambda x: x[-2:])
pres["end"] = pres["end"].map(lambda x: x[-2:])
year_front_start = ["19" for _ in range(9)] + ["20" for _ in range(3)]
year_front_end = ["19" for _ in range(8)] + ["20" for _ in range(4)]
for i in range(len(pres["start"])):
    pres.loc[i, "start"] = int(year_front_start[i] + pres.loc[i, "start"])
    pres.loc[i, "end"] = int(year_front_end[i] + pres.loc[i, "end"]) - 1

def lambda_func1(x):
    for row in pres.iterrows():
        if x >= row[1]["start"] and x <= row[1]["end"]:
            return row[1]["president"]
    return "Not In Dataset"

def lambda_func2(x):
    for row in pres.iterrows():
        if x >= row[1]["start"] and x <= row[1]["end"]:
            return row[1]["party"]
    return "Not In Dataset"

new_unemp['President'] = new_unemp['Year'].map(lambda_func1)
new_unemp['Party'] = new_unemp['Year'].map(lambda_func2)

print(pres)

# for row in new_unemp.iterrows():
#     print(row[1]["Year"])
print(new_unemp)

new_unemp.to_csv("Dataset.csv", index=False)