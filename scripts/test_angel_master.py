from market_analytics.extract.angel_master import fetch_instruments


data = fetch_instruments()


print("Total instruments:", len(data))

print(data[0])