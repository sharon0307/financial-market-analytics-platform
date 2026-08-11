from datetime import datetime

from market_analytics.utils.logger import logger


def parse_timestamp(timestamp):
    """
    Convert SmartAPI timestamp string into Python datetime.

    Example:
    2026-08-04T13:52:00+05:30
    """

    return datetime.fromisoformat(timestamp)



def parse_candle_data(
        instrument_id,
        payload_id,
        data
):
    """
    Convert SmartAPI candle response into
    raw_market_data format.
    """

    logger.info(
        f"Parsing raw candle data for instrument_id={instrument_id} "
        f"(Payload ID={payload_id})."
    )

    records = []

    try:

        for candle in data:

            timestamp = candle[0]

            open_price = candle[1]
            high_price = candle[2]
            low_price = candle[3]
            close_price = candle[4]
            volume = candle[5]

            records.append(
                {
                    "instrument_id": instrument_id,

                    "timestamp": parse_timestamp(
                        timestamp
                    ),

                    "open": open_price,

                    "high": high_price,

                    "low": low_price,

                    "close": close_price,

                    "volume": volume,

                    "payload_id": payload_id
                }
            )

        logger.info(
            f"Parsed {len(records)} candle records."
        )

        return records

    except Exception:

        logger.exception(
            f"Failed to parse candle data for instrument_id={instrument_id}."
        )

        raise