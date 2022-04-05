import pandas as pd
import logging
import sys
import requests
from api_resp_flat import ApiCallFlat
from x_converter import XConverter

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/musem_script.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

url_1 = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
url_2 = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

try:
    data = ApiCallFlat.api_call(url_1)
except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

ids = data["objectIDs"][:10]

api_data = []
for i_d in ids:
    try:
        resp_data = ApiCallFlat.api_call(url_2 + str(i_d))
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as ex:
        logger.error("%s-%s", ex.__class__.__name__, ex)
        sys.exit(1)
    api_data.append(resp_data)

flatten_dfs = []
for data in api_data:
    try:
        flat_dict = ApiCallFlat.flatten_json(data)
    except TypeError as ex:
        logger.error("%s-%s", ex.__class__.__name__, ex)
        sys.exit(1)
    flatten_dfs.append(flat_dict)

flat_data = pd.concat(flatten_dfs, axis=1)
flat_df = flat_data.transpose()


try:
    XConverter(flat_df, "./files/json_html.html").df_html()
except (PermissionError, ValueError, TypeError, OSError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

options = {
    'page-height': '400',
    'page-width': '400',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
}
path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

try:
    XConverter(flat_df, "./files/json_pdf.pdf").df_pdf(htmlfile_name="./files/json_html.html", wkhtmltopdf_path=path)
except (PermissionError, TypeError, ValueError, FileNotFoundError, OSError) as ex:
    logger.error("%s-%s", ex.__class__.__name__, ex)
    sys.exit(1)

# print(flat_df)
