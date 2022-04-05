import requests
import matplotlib.pyplot as plt
import pandas as pd
import logging, inspect

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="./logs/functional_plot1.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()


def bar_plot_api_call():
    """Fetch API data and returns to plot bar graph."""

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=\
               100&page=1&sparkline=false"

    response = requests.get(url)

    logger.debug("Type of response expected of <class list>")
    resp_data = response.json()  # gives dict
    logger.debug("Type of response is %s", type(resp_data))

    data_dic = {}  # stores data from api
    for dic in resp_data[:15]:
        data_dic.update({dic["name"]: dic["current_price"]})

    return data_dic


def bar_plot(dict_data):
    """Plot a bar graph groph from data in dict."""

    name = list(dict_data.keys())
    price = list(dict_data.values())
    plt.figure(figsize=(10, 5))

    logger.debug("Plotting bar graph...")
    # creating the bar plot
    plt.bar(name, price, color='maroon',
            width=0.5)
    plt.xlabel("names")
    plt.ylabel("Prices")
    plt.title("Crypto prices")
    logger.debug("bar graph is Ready!!")
    plt.show()


def api_coin_df():
    """Extracts important data from API and Returns Dataframe."""

    func = inspect.currentframe().f_back.f_code
    message = "Extracts important data to plot from coin api"
    logging.debug("%s: %s in %s:%i" % (
        message,
        func.co_name,
        func.co_filename,
        func.co_firstlineno
    ))
    coin_data = []
    for y in range(2013, 2022):
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=30-12-" + str(y)
        r = requests.get(url)
        data_dict = r.json()  # gives dict
        name = data_dict["name"]
        date = "30-12-" + str(y)
        end_year = y
        price_usd = data_dict["market_data"]["current_price"]["usd"]
        price_inr = data_dict["market_data"]["current_price"]["inr"]
        twitter_followers = data_dict["community_data"]["twitter_followers"]
        if not twitter_followers:
            twitter_followers = 0
        reddit_subscribers = data_dict["community_data"]["reddit_subscribers"]
        if not reddit_subscribers:
            reddit_subscribers = 0
        entity = [name, end_year, date, price_usd, price_inr, twitter_followers, reddit_subscribers]
        coin_data.append(entity)
        df = pd.DataFrame(coin_data,
                          columns=['name', "end_year", 'date', 'price_usd', 'price_inr', 'twitter_followers',
                                   'reddit_subscribers'])
    return df


def scatter_plot(df):
    """Plot Scatter graph from dataframe. """

    logger.debug("Dataframe of extracted file is created")
    plt.rcParams["axes.formatter.limits"] = (0, 5000000)

    # scatter plot
    plt.scatter(df['twitter_followers'], df['price_inr'])

    plt.xlabel("Price in INR")
    plt.ylabel("Twitter followers")
    plt.title("Bitcoin price vs twitter followers")

    plt.show()


def box_plot(df):
    """Plot individual attribute box plot from dataframe."""

    plt.boxplot(df['price_inr'])
    plt.show()


def pi_chart(df):
    """Plot pi plot from dataframe. """
    # Pie plot
    plt.figure(figsize=(10, 7))
    plt.pie(df['reddit_subscribers'], labels=df['end_year'], autopct='% 1.1f %%', shadow=True)
    # show plot
    plt.show()


bar_plot(bar_plot_api_call())

df = api_coin_df()

scatter_plot(df)
box_plot(df)
pi_chart(df)
