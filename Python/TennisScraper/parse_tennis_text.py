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

""" file = open("TennisScraperText.rtf", 'r')

data = file.read()

potential_utr_ids = []

rank_pattern = r"<d2p1:Rank>(\d+)<\/d2p1:Rank>"
birth_year_patten = r"<d2p1:BirthYear>(\d+)<\/d2p1:BirthYear>"
family_name_pattern = r"<d2p1:PlayerFamilyName>(.+)<\/d2p1:PlayerFamilyName>"
given_name_pattern = r"<d2p1:PlayerGivenName>(.+)<\/d2p1:PlayerGivenName>"
rank = re.findall(rank_pattern, data)
birth_year = re.findall(birth_year_patten, data)
family_name = re.findall(family_name_pattern, data)
given_name = re.findall(given_name_pattern, data)

family_name = [name.replace("\\'a0", "") for name in family_name] """

""" df = pd.DataFrame(list(zip(rank, birth_year, family_name, given_name)),
               columns =['rank', 'birth_year', 'family_name', 'given_name'])
 """

df = pd.read_csv("tennis_players.csv")


print(df.shape)

""" file.close()
 """
with open(r'config.yml') as file:
    config = yaml.safe_load(file)

utr_login = config["utr"]["login"]
utr_home = config["utr"]["home"]
utr_profile = config["utr"]["profile_url"]
utr_username = config["utr"]["username"]
utr_password = config["utr"]["password"]

itf_utr_rating = []
for name in tqdm(df["player_name"]):
    itf_utr_rating.append(find_utr_rating_by_name(utr_login, utr_home, name, utr_username, utr_password))
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
itf_df_final = pd.merge(df, itf_utr_rating_player_id_df, left_index=True, right_index=True)
print(itf_df_final)

itf_df_final.to_csv("itf_df_final.csv", index=False)