# Scatter, pie and box plot from api data
import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging,inspect

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/plot2.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()


def api_coin_data():
    """Extracts important data to plot from coin api"""
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
        response = requests.get(url)
        data_dict = response.json()  # gives dict
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
    return coin_data


df = pd.DataFrame(api_coin_data(), columns=['name', "end_year", 'date', 'price_usd', 'price_inr', 'twitter_followers',
                                            'reddit_subscribers'])

logger.debug("Dataframe of extracted file is created")
plt.rcParams["axes.formatter.limits"] = (0, 5000000)

# scatter plot
plt.scatter(df['twitter_followers'], df['price_inr'])
plt.xlabel("Price in INR")
plt.ylabel("Twitter followers")
plt.title("Bitcoin price vs twitter followers")
plt.show()

# individual attribute box plot
plt.boxplot(df['price_inr'])
plt.show()

# Pie plot
fig = plt.figure(figsize=(10, 7))
plt.pie(df['reddit_subscribers'], labels=df['end_year'], autopct='% 1.1f %%', shadow=True)

# show plot
plt.show()
