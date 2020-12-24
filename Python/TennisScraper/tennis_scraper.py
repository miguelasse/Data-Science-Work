from bs4 import BeautifulSoup
import html5lib
import json
import lxml
import pandas as pd
import selenium
import re
import requests
import time
from tqdm import tqdm
import yaml
from utilities import find_utr_ids
from utilities import find_utr_rating
from utilities import find_utr_rating_by_name

with open(r'config.yml') as file:
    config = yaml.safe_load(file)

ids = []
tennis_recruiting_url = config["tennis_recruiting"]["list_url"]
boys_18_id = config["tennis_recruiting"]["boys_18_id"]

page = requests.get(tennis_recruiting_url + boys_18_id)
soup = BeautifulSoup(page.content, "lxml")
table_body = soup.find_all("tbody")

data = pd.read_html("<table>" + str(table_body) + "/<table>")
tennis = data[0][:100]
header = {0:"Rank", 1: "Prev_Rank", 2: "Name", 3: "State", 4: "Stars", 5:"Num_Tournaments"}
tennis = tennis.rename(mapper=header, axis=1)
tennis.drop("Stars", axis=1, inplace=True)

tr_player_ids = []
for row in table_body:    
    cols = row.find_all("a")
    for col in cols:
        id = re.findall("[\d]{6,6}", str(col))
        if len(id) >= 1:
            tr_player_ids.append(int(id[0]))

tr_player_ids = set(tr_player_ids)
tr_player_ids = list(tr_player_ids)
 
tr_player_url = config["tennis_recruiting"]["player_url"]

potential_utr_ids = []
for id in tqdm(tr_player_ids[0:1]):
    page = requests.get(tr_player_url + str(id))
    soup = BeautifulSoup(page.content, "lxml")
    potential_utr_ids.append(find_utr_ids(soup, "script"))

tr_df = pd.DataFrame(potential_utr_ids)
header = {0:"tennis_recruiting_id", 1: "utr_id"}
tr_df = tr_df.rename(mapper=header, axis=1)

tennis = pd.merge(tennis, tr_df, left_index=True, right_index=True)
header = {0:"player_id"}
tennis = tennis.rename(mapper=header,axis=1)

utr_login = config["utr"]["login"]
utr_home = config["utr"]["home"]
utr_profile = config["utr"]["profile_url"]
utr_username = config["utr"]["username"]
utr_password = config["utr"]["password"]

utr_rating = []
for utr_id in tqdm(tennis["utr_id"]):
    utr_rating.append(find_utr_rating(utr_login, utr_profile, utr_id, utr_username, utr_password))

utr_rating_df = pd.DataFrame(utr_rating, columns=["utr_id", "utr_rating"])

itr_url = config["itf"]["api_url"]

cookies_part_1 = str(input("Enter in cookies part 1:"))
cookies_part_2 = str(input("Enter in cookies part 2:"))

page = requests.get(itr_url, cookies={cookies_part_1:cookies_part_2})
soup = BeautifulSoup(page.content, "lxml")
site_json=json.loads(soup.text)

itf_df = pd.DataFrame.from_dict(site_json["items"])
itf_df["playerName"] = itf_df["playerGivenName"] + " " + itf_df["playerFamilyName"]

itf_utr_rating = []
for name in tqdm(itf_df["playerName"]):
    itf_utr_rating.append(find_utr_rating_by_name(utr_login, utr_home, name, utr_username, utr_password))
print(itf_utr_rating)
itf_utr_rating_df = pd.DataFrame(itf_utr_rating)
itf_utr_rating_df_final = itf_utr_rating_df.iloc[:, 0:2]

header = {0:"player_name", 1: "utr_id"}
itf_utr_rating_df_final = itf_utr_rating_df_final.rename(mapper=header, axis=1)
print(itf_utr_rating_df_final)

itf_utr_rating_player_id = []
for utr_id in tqdm(itf_utr_rating_df_final["utr_id"]):
    itf_utr_rating_player_id.append(find_utr_rating(utr_login, utr_profile, utr_id, utr_username, utr_password))

itf_utr_rating_player_id_df = pd.DataFrame(itf_utr_rating_player_id, columns=["utr_id", "utr_rating"])
print(itf_utr_rating_player_id_df)
itf_df_final = pd.merge(itf_df, itf_utr_rating_player_id_df, left_index=True, right_index=True)
print(itf_df_final)

itf_df_final.to_csv("itf_df_final.csv", index=False)
tennis.to_csv("tennis_recruiting_final.csv", index=False)