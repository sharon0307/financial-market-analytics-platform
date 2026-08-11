from market_analytics.extract.smartapi_client import SmartAPIClient

client = SmartAPIClient()

client.login()

print(client.jwt_token is not None)

client.logout()

print(client.smart_api)
print(client.jwt_token)