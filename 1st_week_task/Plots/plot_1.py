# plotting a bar graph

import requests
import matplotlib.pyplot as plt
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logs/plot1.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="w", )
logger = logging.getLogger()

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=\
       100&page=1&sparkline=false"

r = requests.get(url)
logger.debug("Type of response expected of <class list>")
data_list = r.json()  # gives dict
logger.debug("Type of response is %s", type(data_list))
temp_dic = {}  # stores data from api
for dic in data_list[:15]:
    temp_dic.update({dic["name"]: dic["current_price"]})

name = list(temp_dic.keys())
price = list(temp_dic.values())
fig = plt.figure(figsize=(10, 5))

logger.info("Plotting bar graph...")
# creating the bar plot
plt.bar(name, price, color='maroon',
        width=0.5)

plt.xlabel("names")
plt.ylabel("Prices")
plt.title("Crypto prices")

logger.info("bar graph Generated Successfully")
plt.show()


