from datetime import datetime

from market_analytics.extract.download_manager import (
    DownloadManager
)


def main():

    manager = DownloadManager()

    result = manager.download_instrument(
        instrument_id=2052,
        exchange="NSE",
        token="2885",
        interval="ONE_MINUTE",
        start_time=datetime(
            2026,
            8,
            4,
            9,
            15
        ),
        end_time=datetime(
            2026,
            8,
            4,
            15,
            30
        )
    )

    print("\n" + "=" * 60)
    print("DOWNLOAD MANAGER RESULT")
    print("=" * 60)

    print(
        f"Instrument ID: "
        f"{result['instrument_id']}"
    )

    print(
        f"Payloads saved: "
        f"{result['payloads']}"
    )

    print(
        f"Raw rows inserted: "
        f"{result['raw_rows_inserted']}"
    )


if __name__ == "__main__":
    main()