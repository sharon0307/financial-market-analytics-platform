from market_analytics.extract.angel_master import fetch_instruments


data = fetch_instruments()


spot_equities = [
    x for x in data
    if x.get("exch_seg") in ["NSE", "BSE"]
    and x.get("symbol", "").endswith("-EQ")
]


print("Spot Equity Count:", len(spot_equities))


for item in spot_equities[:10]:
    print(item)