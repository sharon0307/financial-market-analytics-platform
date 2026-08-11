import argparse
from datetime import datetime

from market_analytics.extract.historical_downloader import (
    HistoricalDownloader
)


def main():

    parser = argparse.ArgumentParser(
        description="Test HistoricalDownloader date chunking"
    )

    parser.add_argument(
        "--start-date",
        required=True,
        help="Start date in YYYY-MM-DD format"
    )

    parser.add_argument(
        "--end-date",
        required=True,
        help="End date in YYYY-MM-DD format"
    )

    args = parser.parse_args()

    start_time = datetime.strptime(
        args.start_date,
        "%Y-%m-%d"
    )

    end_time = datetime.strptime(
        args.end_date,
        "%Y-%m-%d"
    )

    downloader = HistoricalDownloader()

    chunks = downloader._generate_chunks(
        start_time,
        end_time
    )

    print()
    print("=" * 60)
    print("HISTORICAL DOWNLOADER CHUNK TEST")
    print("=" * 60)

    print(f"Start date   : {start_time}")
    print(f"End date     : {end_time}")
    print(f"Total chunks : {len(chunks)}")
    print()

    for index, (chunk_start, chunk_end) in enumerate(
        chunks,
        start=1
    ):
        print(
            f"Chunk {index}: "
            f"{chunk_start} -> {chunk_end}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()