import argparse
from datetime import datetime

from market_analytics.transform.process_returns import process_returns
from market_analytics.transform.process_vwap import process_vwap
from market_analytics.utils.logger import logger


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d")


def run_analytics(
    instrument_id,
    timeframe,
    start_time,
    end_time
):
    logger.info(
        f"Starting analytics run | "
        f"Instrument={instrument_id} | "
        f"Timeframe={timeframe} | "
        f"From={start_time} | "
        f"To={end_time}"
    )

    returns_rows = 0
    vwap_rows = 0

    try:

        # -------------------------------------------------
        # RETURNS
        # -------------------------------------------------

        logger.info(
            f"Starting Returns analytics | "
            f"Instrument={instrument_id}"
        )

        returns_rows = process_returns(
            instrument_id=instrument_id,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time
        )

        logger.info(
            f"Returns analytics completed | "
            f"Instrument={instrument_id} | "
            f"Inserted={returns_rows}"
        )

        # -------------------------------------------------
        # VWAP
        # -------------------------------------------------

        logger.info(
            f"Starting VWAP analytics | "
            f"Instrument={instrument_id}"
        )

        vwap_rows = process_vwap(
            instrument_id=instrument_id,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time
        )

        logger.info(
            f"VWAP analytics completed | "
            f"Instrument={instrument_id} | "
            f"Inserted={vwap_rows}"
        )

        logger.info(
            f"Analytics run completed successfully | "
            f"Instrument={instrument_id} | "
            f"ReturnsRows={returns_rows} | "
            f"VWAPRows={vwap_rows}"
        )

        return {
            "success": True,
            "instrument_id": instrument_id,
            "returns": returns_rows,
            "vwap": vwap_rows
        }

    except Exception:

        logger.exception(
            f"Analytics run failed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe}"
        )

        return {
            "success": False,
            "instrument_id": instrument_id,
            "returns": returns_rows,
            "vwap": vwap_rows
        }


def main():

    parser = argparse.ArgumentParser(
        description="Run Returns and VWAP analytics"
    )

    parser.add_argument(
        "--instruments",
        nargs="+",
        type=int,
        required=True,
        help="Instrument IDs"
    )

    parser.add_argument(
        "--start",
        required=True,
        help="Start date YYYY-MM-DD"
    )

    parser.add_argument(
        "--end",
        required=True,
        help="End date YYYY-MM-DD"
    )

    parser.add_argument(
        "--timeframe",
        default="5m",
        choices=["2m", "5m", "15m"],
        help="Candle timeframe"
    )

    args = parser.parse_args()

    start_time = parse_date(args.start).replace(
        hour=9,
        minute=15
    )

    end_time = parse_date(args.end).replace(
        hour=15,
        minute=29
    )

    logger.info(
        f"Starting bulk analytics | "
        f"Instruments={args.instruments} | "
        f"Timeframe={args.timeframe} | "
        f"From={start_time} | "
        f"To={end_time}"
    )

    successful = []
    failed = []

    for instrument_id in args.instruments:

        result = run_analytics(
            instrument_id=instrument_id,
            timeframe=args.timeframe,
            start_time=start_time,
            end_time=end_time
        )

        if result["success"]:
            successful.append(result)
        else:
            failed.append(result)

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    print("\n" + "=" * 70)
    print("ANALYTICS RESULT")
    print("=" * 70)

    print(f"Total instruments : {len(args.instruments)}")
    print(f"Successful        : {len(successful)}")
    print(f"Failed            : {len(failed)}")

    if successful:

        print("\n## SUCCESSFUL")

        for result in successful:

            print(
                f"{result['instrument_id']} | "
                f"Returns={result['returns']} | "
                f"VWAP={result['vwap']}"
            )

    if failed:

        print("\n## FAILED")

        for result in failed:

            print(
                f"{result['instrument_id']} | "
                f"Returns={result['returns']} | "
                f"VWAP={result['vwap']}"
            )

    print("=" * 70)


if __name__ == "__main__":
    main()