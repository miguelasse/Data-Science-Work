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

utr_login = config["utr"]["login"]
utr_home = config["utr"]["home"]
utr_profile = config["utr"]["profile_url"]
utr_username = config["utr"]["username"]
utr_password = config["utr"]["password"]

itf_df = pd.read_csv(config["itf"]["csv_name"])
itf_utr_rating = []

for name in tqdm(itf_df["player_name"]):
    itf_utr_rating.append(find_utr_rating_by_name(utr_login, utr_home, name, utr_username, utr_password))

itf_utr_rating_df = pd.DataFrame(itf_utr_rating)
itf_utr_rating_df_final = itf_utr_rating_df.iloc[:, 0:2]

header = {0:"player_name", 1: "utr_id"}
itf_utr_rating_df_final = itf_utr_rating_df_final.rename(mapper=header, axis=1)

itf_utr_rating_player_id = []
for utr_id in tqdm(itf_utr_rating_df_final["utr_id"]):
    itf_utr_rating_player_id.append(find_utr_rating(utr_login, utr_profile, utr_id, utr_username, utr_password))

itf_utr_rating_player_id_df = pd.DataFrame(itf_utr_rating_player_id, columns=["utr_id", "utr_rating"])
itf_df_final = pd.merge(itf_df, itf_utr_rating_player_id_df, left_index=True, right_index=True)
itf_df_final.to_csv("itf_df_final.csv", index=False)