
import re
import yaml
import pandas as pd

with open(r'config.yml') as file:
    config = yaml.safe_load(file)

text = open(config["itf"]["text_file_name"], "r")
data = text.read()

birth_year = re.findall("(?<=BirthYear>)(.*)(?=<\/d2p1)", data)
last_name = re.findall("(?<=PlayerFamilyName>)(.*)(?=<\/d2p1)", data)
first_name = re.findall("(?<=PlayerGivenName>)(.*)(?=<\/d2p1)", data)
player_id = re.findall("(?<=PlayerId>)(.*)(?=<\/d2p1)", data)
player_country_code = re.findall("(?<=PlayerNationalityCode>)(.*)(?=<\/d2p1)", data)


dataframe = pd.DataFrame(list(zip(
    birth_year, 
    last_name,
    first_name,
    player_country_code)))

rename_cols = {0:"birth_year", 1:"last_name", 2:"first_name",
              3:"player_country_code"}

data_final = dataframe.rename(columns=rename_cols)

data_final["player_name"] = data_final["first_name"] + " " + data_final["last_name"]

data_final.head()

data_final_birth_year = data_final[data_final["birth_year"] == config["itf"]["birth_year"]]

data_final_birth_year.to_csv("data_final_" + config["itf"]["birth_year"] + ".csv", index=False)