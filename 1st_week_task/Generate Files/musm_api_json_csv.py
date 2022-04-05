# Writing flatten dict data to csv from api

import requests
import pandas as pd
from flatten_json import flatten
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/musm.api_json_csv.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
logger.debug("Type of response expected of class <Dict>")
data_dict = response.json()  # gives dict
logger.debug("Type of response is %s", type(data_dict))
ids = data_dict["objectIDs"][:10]
dfs = []  # stores all df

# Converting response objects to flat dict dataframe
for i_d in ids:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(i_d)
    response = requests.get(url)
    logger.debug("Type of response expected of class <Dict>")
    data_dict = response.json()  # gives dict
    logger.debug("Type of response is %s", type(data_dict))

    flatten_dict = flatten(data_dict)
    logger.info("flattening dict...")
    # df = pd.DataFrame.from_dict(flatten_dict, orient='index')  # dict to df
    df = pd.DataFrame([flatten_dict.values()], columns=flatten_dict.keys())
    dfs.append(df)

logger.info("All dataframes are stored in seperate list")

data = pd.concat(dfs, ignore_index=True)
logger.info("Generating CSV...")
data.to_csv('./files/museum_json.csv', index=False, index_label=True, encoding='utf-8-sig')
logger.info("CSV file generated Successfully")



