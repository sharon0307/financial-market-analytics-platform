from datetime import datetime

from market_analytics.extract.historical_downloader import (
    HistoricalDownloader
)


def main():

    downloader = HistoricalDownloader()

    start_time = datetime(2026, 8, 4, 9, 15)
    end_time = datetime(2026, 8, 4, 15, 30)

    for chunk in downloader.download(
        exchange="NSE",
        token="2885",
        interval="ONE_MINUTE",
        start_time=start_time,
        end_time=end_time
    ):

        print("\n" + "=" * 60)
        print("CHUNK RESULT")
        print("=" * 60)

        print(
            f"Chunk: {chunk['chunk_number']}/"
            f"{chunk['total_chunks']}"
        )

        print(
            f"Start: {chunk['start_time']}"
        )

        print(
            f"End:   {chunk['end_time']}"
        )

        print(
            f"Candles received: "
            f"{len(chunk['data'])}"
        )

        if chunk["data"]:

            print("\nFirst candle:")
            print(chunk["data"][0])

            print("\nLast candle:")
            print(chunk["data"][-1])


if __name__ == "__main__":
    main()