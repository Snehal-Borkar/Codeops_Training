# Writes api data to xml file

import requests
import pandas as pd
from json2xml import json2xml
from json2xml.utils import readfromstring
import json
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/json_xml.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()


r = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
logger.debug("Type of response expected of class <Dict>")
data_dict = r.json()  # gives dict
logger.debug("Type of response is %s", type(data_dict))
ids = data_dict["objectIDs"][:10]
dfs = []  # to store all df

for i_d in ids:
    url = "https://collectionapi.metmuseum.org/public/collection   /v1/objects/" + str(i_d)
    response = requests.get(url)

    logger.debug("Type of response expected of class <Dict>")
    data_dict = response.json()  # gives dict
    logger.debug("Type of response is %s", type(data_dict))

    df = pd.DataFrame.from_dict(data_dict, orient='index')
    dfs.append(df)

data = pd.concat(dfs, axis=1)
new_un_flat_df = data.transpose()
new_un_flat_dict = new_un_flat_df.to_dict(orient='records')
json_str = json.dumps(new_un_flat_dict)

data = readfromstring(json_str)

logger.info("Converting to xml...")
xml_data = json2xml.Json2xml(data).to_xml()  # get the xml from a json string
logger.info("Writing to xml...")

with open("files/json_xml.xml", "w") as xml_file:
    xml_file.write(xml_data)
logger.info("xml file generated Successfully")
