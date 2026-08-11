from datetime import datetime

from market_analytics.transform.process_1m import process_1m


process_1m(
    instrument_id=2052,
    start_time=datetime(2026,8,7,9,15),
    end_time=datetime(2026,8,10,15,30)
)