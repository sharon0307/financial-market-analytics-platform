import argparse
from datetime import datetime

from market_analytics.database.connection import SessionLocal
from market_analytics.database.models import Instrument

from market_analytics.extract.download_manager import DownloadManager
from market_analytics.transform.process_1m import process_1m

from market_analytics.utils.logger import logger


def get_instruments(instrument_ids):
    """
    Fetch instruments from the database.
    """

    session = SessionLocal()

    try:

        instruments = (
            session.query(Instrument)
            .filter(
                Instrument.id.in_(instrument_ids)
            )
            .order_by(
                Instrument.id
            )
            .all()
        )

        found_ids = {
            instrument.id
            for instrument in instruments
        }

        missing_ids = [
            instrument_id
            for instrument_id in instrument_ids
            if instrument_id not in found_ids
        ]

        if missing_ids:

            raise ValueError(
                f"Instruments not found in DB: "
                f"{missing_ids}"
            )

        return instruments

    finally:

        session.close()


def download_instrument(
    manager,
    instrument,
    start_time,
    end_time
):
    """
    Download historical 1-minute data
    for one instrument.
    """

    logger.info(
        f"Starting download | "
        f"Instrument={instrument.id} | "
        f"Symbol={instrument.symbol} | "
        f"Token={instrument.token}"
    )

    result = manager.download_instrument(
        instrument_id=instrument.id,
        exchange=instrument.exchange,
        token=instrument.token,
        interval="ONE_MINUTE",
        start_time=start_time,
        end_time=end_time
    )

    return result


def process_instrument(
    instrument,
    start_time,
    end_time
):
    """
    Process downloaded raw 1-minute data.
    """

    logger.info(
        f"Starting processing | "
        f"Instrument={instrument.id} | "
        f"Symbol={instrument.symbol}"
    )

    inserted = process_1m(
        instrument_id=instrument.id,
        start_time=start_time,
        end_time=end_time
    )

    return inserted


def parse_arguments():

    parser = argparse.ArgumentParser(
        description=(
            "Download and process historical "
            "1-minute market data."
        )
    )

    parser.add_argument(
        "--instruments",
        nargs="+",
        type=int,
        required=True,
        help=(
            "Instrument database IDs. "
            "Example: --instruments 2052 2053"
        )
    )

    parser.add_argument(
        "--start",
        required=True,
        help=(
            "Start date in YYYY-MM-DD format. "
            "Example: 2026-08-04"
        )
    )

    parser.add_argument(
        "--end",
        required=True,
        help=(
            "End date in YYYY-MM-DD format. "
            "Example: 2026-08-06"
        )
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    # --------------------------------------------------------
    # DATE VALIDATION
    # --------------------------------------------------------

    try:

        start_time = datetime.strptime(
            args.start,
            "%Y-%m-%d"
        ).replace(
            hour=9,
            minute=15
        )

        end_time = datetime.strptime(
            args.end,
            "%Y-%m-%d"
        ).replace(
            hour=15,
            minute=30
        )

    except ValueError:

        raise ValueError(
            "Dates must use YYYY-MM-DD format."
        )

    if start_time > end_time:

        raise ValueError(
            "Start date cannot be after end date."
        )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("HISTORICAL MARKET DATA PIPELINE")
    print("=" * 70)
    print(
        f"Instruments : {args.instruments}"
    )
    print(
        f"Start       : {start_time}"
    )
    print(
        f"End         : {end_time}"
    )
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # LOAD INSTRUMENTS
    # --------------------------------------------------------

    instruments = get_instruments(
        args.instruments
    )

    print(
        f"Found {len(instruments)} instruments."
    )

    # --------------------------------------------------------
    # CREATE DOWNLOAD MANAGER
    # --------------------------------------------------------

    manager = DownloadManager()

    successful = []
    failed = []

    # --------------------------------------------------------
    # PROCESS ONE INSTRUMENT AT A TIME
    # --------------------------------------------------------

    for instrument in instruments:

        print()
        print("-" * 70)
        print(
            f"Instrument: {instrument.id} | "
            f"{instrument.symbol} | "
            f"Token={instrument.token}"
        )
        print("-" * 70)

        try:

            # ------------------------------------------------
            # DOWNLOAD
            # ------------------------------------------------

            download_result = download_instrument(
                manager=manager,
                instrument=instrument,
                start_time=start_time,
                end_time=end_time
            )

            logger.info(
                f"Download completed | "
                f"Instrument={instrument.id}"
            )

            # ------------------------------------------------
            # PROCESS
            # ------------------------------------------------

            processed_rows = process_instrument(
                instrument=instrument,
                start_time=start_time,
                end_time=end_time
            )

            logger.info(
                f"Processing completed | "
                f"Instrument={instrument.id} | "
                f"Inserted={processed_rows}"
            )

            successful.append(
                {
                    "id": instrument.id,
                    "symbol": instrument.symbol,
                    "token": instrument.token,
                    "processed": processed_rows
                }
            )

        except Exception as exc:

            logger.exception(
                f"Pipeline failed | "
                f"Instrument={instrument.id} | "
                f"Symbol={instrument.symbol}"
            )

            failed.append(
                {
                    "id": instrument.id,
                    "symbol": instrument.symbol,
                    "token": instrument.token,
                    "error": str(exc)
                }
            )

            # Important:
            # Continue with the next instrument.
            continue

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)

    print(
        f"Total instruments : "
        f"{len(instruments)}"
    )

    print(
        f"Successful        : "
        f"{len(successful)}"
    )

    print(
        f"Failed            : "
        f"{len(failed)}"
    )

    print()

    if successful:

        print("SUCCESSFUL")
        print("-" * 70)

        for item in successful:

            print(
                f"{item['id']:>6} | "
                f"{item['symbol']:<25} | "
                f"Processed={item['processed']}"
            )

    if failed:

        print()
        print("FAILED")
        print("-" * 70)

        for item in failed:

            print(
                f"{item['id']:>6} | "
                f"{item['symbol']:<25} | "
                f"{item['error']}"
            )

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()