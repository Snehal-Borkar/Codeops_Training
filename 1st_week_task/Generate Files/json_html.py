# Calling api and converting python object into html table page.

import requests
import pandas as pd
from flatten_json import flatten
import logging,inspect

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/json_html.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
logger.debug("Type of response expected of class <List>")
data_dict = response.json()  # gives dict
logger.debug("Type of response is %s", type(data_dict))
ids = data_dict["objectIDs"][40:55]   # list of ids to be called
dfs = []  # to store all df

# json from api to flat dict df
for i_d in ids:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(i_d)
    response = requests.get(url)
    logger.debug("Type of response expected of class <Dict>")
    data_dict = response.json()  # gives dict
    logger.debug("Type of response is %s", type(data_dict))
    flatten_dict = flatten(data_dict)
    df = pd.DataFrame.from_dict(flatten_dict, orient='index')  # dict to df
    dfs.append(df)


data = pd.concat(dfs, axis=1)
new_df = data.transpose()
logger.info("dataframes containing all data created")


def path_to_image_html(path):
    """Values from dataframe are edited or changes format."""

    return '<img src="' + path + '" width="60" >'


logger.info("Converting to HTML.")

new_df.to_html('./files/json_html.html', escape=False, index=False, encoding="utf-8-sig",
               formatters=dict(primaryImage=path_to_image_html, primaryImageSmall=path_to_image_html,
                               additionalImages_0=path_to_image_html))
logger.info("HTML file is Ready to Open !.")
