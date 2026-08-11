from market_analytics.database.connection import get_connection
from market_analytics.database.models import ProcessedMarketData



get_connection()

print(ProcessedMarketData.__tablename__)