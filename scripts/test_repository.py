from market_analytics.database.repositories.instrument_repository import (
    get_all_instruments, get_by_symbol, get_by_token, get_spot_equities
)

rows = get_all_instruments()

print(f"Total: {len(rows)}")

print(rows[0])


spots = get_spot_equities()

print(f"Spot instruments: {len(spots)}")
print(spots[:5])