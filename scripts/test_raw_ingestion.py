from datetime import datetime

from market_analytics.extract.historical_downloader import (
    HistoricalDownloader
)

from market_analytics.extract.raw_loader import (
    parse_candle_data
)

from market_analytics.database.repositories.raw_repository import (
    save_raw_payload,
    save_raw_market_data,
    get_raw_market_data
)


def test_raw_ingestion(
    start_time,
    end_time
):

    instrument_id = 2052
    token = "2885"

    downloader = HistoricalDownloader()

    total_candles = 0
    total_inserted = 0
    payload_ids = []

    for chunk in downloader.download(
        exchange="NSE",
        token=token,
        interval="ONE_MINUTE",
        start_time=start_time,
        end_time=end_time
    ):

        print("\n" + "=" * 60)
        print("CHUNK")
        print("=" * 60)

        print(
            "Chunk:",
            f"{chunk['chunk_number']}/{chunk['total_chunks']}"
        )

        print(
            "From:",
            chunk["start_time"]
        )

        print(
            "To:",
            chunk["end_time"]
        )

        candles = chunk["data"]

        print(
            "Candles received:",
            len(candles)
        )

        total_candles += len(candles)

        # --------------------------------------------------
        # 1. Save original SmartAPI response
        # --------------------------------------------------

        payload_id = save_raw_payload(
            instrument_id=instrument_id,
            source="SMARTAPI",
            interval="ONE_MINUTE",
            request_from=chunk["start_time"],
            request_to=chunk["end_time"],
            payload=chunk["response"]
        )

        payload_ids.append(payload_id)

        print(
            "Payload saved:",
            payload_id
        )

        # --------------------------------------------------
        # 2. Parse candles
        # --------------------------------------------------

        records = parse_candle_data(
            instrument_id=instrument_id,
            payload_id=payload_id,
            data=candles
        )

        print(
            "Parsed records:",
            len(records)
        )

        # --------------------------------------------------
        # 3. Save raw market data
        # --------------------------------------------------

        inserted = save_raw_market_data(
            records
        )

        total_inserted += inserted

        print(
            "Raw rows inserted:",
            inserted
        )

    # ------------------------------------------------------
    # Final verification
    # ------------------------------------------------------

    print("\n" + "=" * 60)
    print("RAW INGESTION RESULT")
    print("=" * 60)

    print(
        "Total candles received:",
        total_candles
    )

    print(
        "Total raw rows inserted:",
        total_inserted
    )

    print(
        "Payloads saved:",
        len(payload_ids)
    )

    assert total_candles > 0
    assert len(payload_ids) > 0

    # ------------------------------------------------------
    # Verify database contents
    # ------------------------------------------------------

    saved = get_raw_market_data(
        instrument_id,
        start_time,
        end_time
    )

    print(
        "Database rows:",
        len(saved)
    )

    assert len(saved) > 0

    print(
        "First timestamp:",
        saved[0].timestamp
    )

    print(
        "Last timestamp:",
        saved[-1].timestamp
    )


if __name__ == "__main__":

    test_raw_ingestion(
        start_time=datetime(
            2026,
            8,
            10,
            9,
            15
        ),
        end_time=datetime(
            2026,
            8,
            10,
            15,
            30
        )
    )