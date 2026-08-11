from market_analytics.extract.smartapi_client import SmartAPIClient


client = SmartAPIClient()

client.login()

response = client.smart_api.getCandleData(
    {
        "exchange": "NSE",
        "symboltoken": "2885",
        "interval": "ONE_MINUTE",
        "fromdate": "2026-08-05 09:15",
        "todate": "2026-08-05 15:30"
    }
)


print(response)