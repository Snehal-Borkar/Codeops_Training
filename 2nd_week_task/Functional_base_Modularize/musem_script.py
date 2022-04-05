import pandas as pd
import logging
import api_response
import sys
import requests
import json_X_converter
LOG_FORMAT = "%(lineno)d %(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/musem_script.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

url_1 = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
url_2 = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

try:
    data = api_response.api_call(url_1)
except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
    sys.exit(1)

ids = data["objectIDs"][:10]

api_data = []
for i_d in ids:
    try:
        resp_data = api_response.api_call(url_2 + str(i_d))
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
        logger.error("%s-%s", ex.__class__.__name__, ex)
        sys.exit(1)
    api_data.append(resp_data)
# print(api_data)
flatten_dfs = []
for data in api_data:
    try:
        flat_df = api_response.flatten_json(data)
    except TypeError as ex:
        logger.error("%s-%s", ex.__class__.__name__, ex)
        sys.exit(1)

    flatten_dfs.append(flat_df)

flat_data = pd.concat(flatten_dfs, axis=1)
flat_dfs = flat_data.transpose()


try:
    json_X_converter.df_csv(flat_dfs, "./files/json_csv.csv")
except (PermissionError, ValueError, TypeError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

try:
    json_X_converter.df_html(flat_dfs, "./files/json_html.html")
except (PermissionError, ValueError, TypeError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

try:
    json_X_converter.df_xml(flat_dfs, "./files/json_xml.xml")
except (PermissionError, ValueError, TypeError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

