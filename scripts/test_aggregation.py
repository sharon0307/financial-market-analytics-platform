import argparse
from datetime import datetime

from market_analytics.transform.process_candle import process_candles
from market_analytics.database.models import Candle2M, Candle5M


TIMEFRAME_MODELS = {
    "2min": Candle2M,
    "5min": Candle5M,
}


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d")


def main():

    parser = argparse.ArgumentParser(
        description="Test candle aggregation for multiple instruments"
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
        "--timeframes",
        nargs="+",
        choices=["2min", "5min"],
        default=["2min"],
        help="Candle timeframes"
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

    print("=" * 70)
    print("CANDLE AGGREGATION TEST")
    print("=" * 70)

    print(f"Instruments : {args.instruments}")
    print(f"From        : {start_time}")
    print(f"To          : {end_time}")
    print(f"Timeframes  : {args.timeframes}")

    total_success = 0
    total_failed = 0

    for instrument_id in args.instruments:

        print("\n" + "-" * 70)
        print(f"Instrument: {instrument_id}")
        print("-" * 70)

        for timeframe in args.timeframes:

            candle_model = TIMEFRAME_MODELS[timeframe]

            print(
                f"\nProcessing {timeframe} | "
                f"Instrument={instrument_id}"
            )

            try:

                inserted = process_candles(
                    instrument_id=instrument_id,
                    start_time=start_time,
                    end_time=end_time,
                    timeframe=timeframe,
                    candle_model=candle_model,
                )

                print(
                    f"SUCCESS | "
                    f"Instrument={instrument_id} | "
                    f"Timeframe={timeframe} | "
                    f"Inserted={inserted}"
                )

                total_success += 1

            except Exception as exc:

                print(
                    f"FAILED | "
                    f"Instrument={instrument_id} | "
                    f"Timeframe={timeframe} | "
                    f"Error={exc}"
                )

                total_failed += 1

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(f"Successful: {total_success}")
    print(f"Failed    : {total_failed}")

    print("=" * 70)


if __name__ == "__main__":
    main()