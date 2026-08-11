from datetime import datetime

from market_analytics.transform.process_returns import (
    process_returns
)


process_returns(
    instrument_id=186,
    timeframe="5m",
    start_time=datetime(2026,8,4,9,15),
    end_time=datetime(2026,8,5,15,29)
)