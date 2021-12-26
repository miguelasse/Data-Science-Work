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


data = pd.read_csv("kalamazoo_18s.csv")

utr_login = config["utr"]["login"]
utr_home = config["utr"]["home"]
utr_profile = config["utr"]["profile_url"]
utr_username = config["utr"]["username"]
utr_password = config["utr"]["password"]

utr_rating = []
for name in tqdm(data["player_name"]):
    utr_rating.append(find_utr_rating_by_name(utr_login, utr_home, name, utr_username, utr_password))
utr_rating_df = pd.DataFrame(utr_rating)
utr_rating_df_final = utr_rating_df.iloc[:, 0:2]

header = {0:"player_name", 1: "utr_id"}
utr_rating_df_final = utr_rating_df_final.rename(mapper=header, axis=1)
print(utr_rating_df_final)

utr_rating_player_id = []
for utr_id in tqdm(utr_rating_df_final["utr_id"]):
    utr_rating_player_id.append(find_utr_rating(utr_login, utr_profile, utr_id, utr_username, utr_password))

utr_rating_player_id_df = pd.DataFrame(utr_rating_player_id, columns=["utr_id", "utr_rating"])
print(utr_rating_player_id_df)
kalamazoo_df_final = pd.merge(utr_rating_df_final, utr_rating_player_id_df, how='left', on='utr_id')
print(kalamazoo_df_final)

kalamazoo_df_final.to_csv("kalamazoo_df_final.csv", index=False)