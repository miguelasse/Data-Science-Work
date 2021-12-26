from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import re
import requests
import smtplib
import ssl
import yaml

with open(r'config.yml') as file:
    config = yaml.safe_load(file)
url = config["shelter_luv"]["url"]

print("grabbing doggos...")
# ADD DOG LINKS to email and overall URL
def find_doggos(url): 
    # get HTML through requests
    r = requests.get(url)
    page = r.text
    # Gather all names of dogs
    names = re.findall('(?<=title_tab">)(.*)<', page)
    urls = re.findall('(?<="profile_link")(.*)(?=>)', page)
    # Convert names to a sorted list
    names_list = list(zip(names, urls))
    # Convert names to a Pandas dataframe and rename columns
    dogs_df = pd.DataFrame(names_list, columns=["dog_name", "url"], dtype=str)
    # Return name_df
    return dogs_df

print("organizing doggos...")
old_doggos = pd.read_csv("old_doggos.csv", dtype={"dog_name":str})

new_doggos = find_doggos(url)
new_doggos["url"] = new_doggos["url"].str.extract(r'(?<=href=")(.*)(?=")')

doggo_diffs = new_doggos[~new_doggos['dog_name'].isin(old_doggos["dog_name"])]
number_of_new_dogs = str(len(doggo_diffs))

if number_of_new_dogs == "0":
    print("No new dogs...ending program")
    exit()
else:
    pass

dog_names = ""
dog_urls = ""
for name in doggo_diffs["dog_name"]:
    dog_names += str(name) + ", "

for url in doggo_diffs["url"]:
    dog_urls += str(url) + ", "

dog_df = doggo_diffs.copy()
dog_df["dog_name_url"] = "<a href=" + "'" + dog_df["url"] + "'>" + dog_df["dog_name"] + "</a>"

dog_name_urls = ""
for url in dog_df["dog_name_url"]:
    dog_name_urls += str(url) + ", "

print("sending doggo email...")
port = 465  # For SSL
password = config["gmail"]["application_specific_password"]
sender_email = config["gmail"]["sender_email"]
receiver_email = config["gmail"]["receiver_email"]

# Create a secure SSL context
context = ssl.create_default_context()

message = MIMEMultipart("alternative")
message["Subject"] = "New Doggos!"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
There are """ + number_of_new_dogs + " " + "to check out!" + """\
    
Check out the dogs:\n """ + "\n" + dog_names + dog_urls + "\n\n" + "your new best friends!" + "\n" + """\
    
Regards,
Find Doggos Program"""

html = """\
<html>
<body>
    <p>Hi,<br>
    There are """ + number_of_new_dogs + " " + "to check out!<br>" + """\
    <br>Check out the dogs:\n """ + "\n" + dog_name_urls + "<br><br>" + """\
        
    your new best friends! """ + "<br><br>" + """\

    Regards,<br>
    Find Doggos Program
    </p>
</body>
</html>
"""
# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
    server.quit()


new_doggos.to_csv("old_doggos.csv", index=False)
print("doggos program complete!")
