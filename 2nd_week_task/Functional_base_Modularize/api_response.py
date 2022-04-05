
import pandas as pd
import logging
import requests
from flatten_json import flatten


logger = logging.getLogger()


def api_call(url):
    """
    Make HTTP request and fetch data from response.

    Parameters:
    url (str): url is an Api for fetching json data.

    Returns:
    resp_data (json): json response of API .
    """

    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("%s : Http Connection Successfull - %s", url, response.status_code)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as ex:
        logging.error("%s : %s", ex.__class__.__name__, ex)
        raise requests.exceptions.ConnectionError("%s", ex)
    except requests.exceptions.HTTPError as ex:
        logging.error("%s : %s", ex.__class__.__name__, ex)
        raise requests.exceptions.HTTPError("%s", ex)

    resp_data = response.json()


    return resp_data


def flatten_json(resp_data):
    """
    Converts notmal json data to flat Dataframe.

    Parameters:
    resp_data (json): Json data fetched from API

    Returns:
    flatten_df (pandas.Dataframe)

    """
    if type(resp_data) != dict:
        raise TypeError("Type of resp_data must be of <class: dict>. not %s" % type(resp_data))

    flatten_dict = flatten(resp_data)
    flatten_df = pd.DataFrame.from_dict(flatten_dict, orient='index')  # dict to df

    return flatten_df




