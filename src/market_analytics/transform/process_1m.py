import pandas as pd
from datetime import timedelta, datetime

from market_analytics.database.repositories.raw_repository import (
    get_raw_market_data
)

from market_analytics.database.repositories.processed_repository import (
    save_processed_market_data,
    get_previous_close
)

from market_analytics.utils.logger import logger


def generate_trading_minutes(trading_date):
    """
    Generate the complete NSE trading-minute calendar.

    09:15 through 15:29 inclusive = 375 minutes.
    """

    timestamps = []

    current = datetime.combine(
        trading_date,
        datetime.min.time()
    ).replace(
        hour=9,
        minute=15
    )

    end = datetime.combine(
        trading_date,
        datetime.min.time()
    ).replace(
        hour=15,
        minute=29
    )

    while current <= end:
        timestamps.append(current)
        current += timedelta(minutes=1)

    return timestamps


def raw_to_dataframe(raw_records):
    """
    Convert raw SQLAlchemy records into a pandas DataFrame.
    """

    data = []

    for row in raw_records:

        data.append(
            {
                "timestamp": row.timestamp,
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "volume": row.volume,
                "source_raw_id": row.id
            }
        )

    return pd.DataFrame(data)


def fill_missing_minutes(
    df,
    trading_minutes,
    previous_close=None
):
    """
    Fill missing minutes inside a trading day.

    If the first minute of the day is missing,
    previous_close from the previous trading day is used.

    Missing minutes are represented as:
        open  = previous close
        high  = previous close
        low   = previous close
        close = previous close
        volume = 0
        source_raw_id = None
    """

    calendar = pd.DataFrame(
        {
            "timestamp": trading_minutes
        }
    )

    # Important:
    # An empty DataFrame must still contain the expected columns.
    if df.empty:

        df = pd.DataFrame(
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "source_raw_id"
            ]
        )

    merged = calendar.merge(
        df,
        on="timestamp",
        how="left"
    )

    merged.sort_values(
        "timestamp",
        inplace=True
    )

    current_previous_close = previous_close

    missing_count = 0

    for index, row in merged.iterrows():

        if pd.isna(row["close"]):

            if current_previous_close is not None:

                merged.loc[index, "open"] = current_previous_close
                merged.loc[index, "high"] = current_previous_close
                merged.loc[index, "low"] = current_previous_close
                merged.loc[index, "close"] = current_previous_close
                merged.loc[index, "volume"] = 0
                merged.loc[index, "source_raw_id"] = None

                missing_count += 1

        else:

            current_previous_close = row["close"]

    logger.info(
        f"Missing minutes filled: {missing_count}"
    )

    return merged


def generate_trading_dates(
    start_time,
    end_time
):
    """
    Generate dates between start and end.

    NOTE:
    This currently generates calendar dates.
    We will replace this with the project's actual
    NSE trading calendar before bulk production.
    """

    dates = []

    current = start_time.date()

    while current <= end_time.date():

        dates.append(current)

        current += timedelta(days=1)

    return dates


def process_single_day(
    instrument_id,
    trading_date
):
    """
    Process one trading day for one instrument.
    """

    try:

        day_start = datetime.combine(
            trading_date,
            datetime.min.time()
        ).replace(
            hour=9,
            minute=15
        )

        day_end = datetime.combine(
            trading_date,
            datetime.min.time()
        ).replace(
            hour=15,
            minute=29
        )

        logger.info(
            f"Processing day | "
            f"Instrument={instrument_id} | "
            f"Date={trading_date}"
        )

        # ---------------------------------------------------------
        # 1. Get raw market data
        # ---------------------------------------------------------

        raw_records = get_raw_market_data(
            instrument_id,
            day_start,
            day_end
        )

        logger.info(
            f"Raw records fetched: {len(raw_records)}"
        )

        # ---------------------------------------------------------
        # 2. If entire day has no raw data, skip it
        # ---------------------------------------------------------

        if not raw_records:

            logger.warning(
                f"No raw market data found | "
                f"Instrument={instrument_id} | "
                f"Date={trading_date} | "
                f"Skipping processing"
            )

            return 0

        # ---------------------------------------------------------
        # 3. Get previous processed close
        # ---------------------------------------------------------

        previous_close = get_previous_close(
            instrument_id,
            day_start
        )

        logger.info(
            f"Previous close: {previous_close}"
        )

        # ---------------------------------------------------------
        # 4. Convert raw records to DataFrame
        # ---------------------------------------------------------

        df = raw_to_dataframe(
            raw_records
        )

        # ---------------------------------------------------------
        # 5. Generate complete trading calendar
        # ---------------------------------------------------------

        trading_minutes = generate_trading_minutes(
            trading_date
        )

        # ---------------------------------------------------------
        # 6. Fill missing minutes
        # ---------------------------------------------------------

        processed = fill_missing_minutes(
            df,
            trading_minutes,
            previous_close
        )

        # ---------------------------------------------------------
        # 7. Convert DataFrame to database records
        # ---------------------------------------------------------

        records = []

        for _, row in processed.iterrows():

            # If a missing candle occurs at the beginning
            # and there is no previous close, skip it.
            if pd.isna(row["close"]):

                logger.warning(
                    f"Unable to fill missing candle | "
                    f"Instrument={instrument_id} | "
                    f"Timestamp={row['timestamp']} | "
                    f"No previous close available"
                )

                continue

            records.append(
                {
                    "instrument_id": instrument_id,
                    "timestamp": row["timestamp"],
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": int(row["volume"]),
                    "lastclose": previous_close,
                    "source_raw_id":
                        None
                        if pd.isna(row["source_raw_id"])
                        else int(row["source_raw_id"])
                }
            )

        logger.info(
            f"Processed records generated: {len(records)}"
        )

        # ---------------------------------------------------------
        # 8. Save processed data
        # ---------------------------------------------------------

        if not records:

            logger.warning(
                f"No processed records generated | "
                f"Instrument={instrument_id} | "
                f"Date={trading_date}"
            )

            return 0

        inserted = save_processed_market_data(
            records
        )

        logger.info(
            f"Processed data saved | "
            f"Inserted={inserted}"
        )

        return inserted

    except Exception:

        logger.exception(
            f"Failed processing day | "
            f"Instrument={instrument_id} | "
            f"Date={trading_date}"
        )

        raise


def process_1m(
    instrument_id,
    start_time,
    end_time
):
    """
    Process 1-minute raw data for one instrument
    over a date range.
    """

    logger.info(
        f"Starting 1m processing | "
        f"Instrument={instrument_id} | "
        f"From={start_time} | "
        f"To={end_time}"
    )

    trading_dates = generate_trading_dates(
        start_time,
        end_time
    )

    logger.info(
        f"Trading days to process: {len(trading_dates)}"
    )

    total_inserted = 0

    for trading_date in trading_dates:

        inserted = process_single_day(
            instrument_id,
            trading_date
        )

        total_inserted += inserted

    logger.info(
        f"1m processing completed | "
        f"Instrument={instrument_id} | "
        f"Inserted={total_inserted}"
    )

    return total_inserted