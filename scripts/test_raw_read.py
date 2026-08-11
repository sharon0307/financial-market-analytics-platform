from datetime import datetime

from market_analytics.database.repositories.raw_repository import (
    get_raw_market_data
)


data = get_raw_market_data(
    instrument_id=186,
    start_time=datetime(2026,8,4,9,15),
    end_time=datetime(2026,8,4,15,30)
)


print("Rows:", len(data))


for row in data[:5]:
    print(
        row.timestamp,
        row.open,
        row.close
    )