import pandas as pd

from market_analytics.utils.logger import logger



SUPPORTED_TIMEFRAMES = {
    "2min",
    "3min",
    "5min",
    "15min"
}



def aggregate_candles(
        processed_data,
        timeframe
):
    """
    Convert processed 1-minute market data
    into OHLC candles.

    Parameters
    ----------
    processed_data:
        List of ProcessedMarketData ORM objects

    timeframe:
        Pandas resample frequency.

    Returns
    -------
    list[dict]
        Aggregated candle records
    """



    if timeframe not in SUPPORTED_TIMEFRAMES:

        logger.error(
            f"Unsupported candle timeframe | "
            f"Timeframe={timeframe}"
        )

        raise ValueError(
            f"Unsupported timeframe: {timeframe}"
        )



    if not processed_data:

        logger.warning(
            f"No processed data received for "
            f"candle aggregation | "
            f"Timeframe={timeframe}"
        )

        return []



    logger.info(
        f"Starting candle aggregation | "
        f"Timeframe={timeframe} | "
        f"InputRows={len(processed_data)}"
    )



    try:


        rows = []



        for row in processed_data:


            rows.append(
                {
                    "timestamp": row.timestamp,

                    "open": row.open,

                    "high": row.high,

                    "low": row.low,

                    "close": row.close,

                    "volume": row.volume,

                    "lastclose": row.lastclose
                }
            )



        df = pd.DataFrame(rows)



        if df.empty:

            logger.warning(
                f"Empty dataframe after conversion | "
                f"Timeframe={timeframe}"
            )

            return []



        if df["timestamp"].isna().any():

            logger.warning(
                "Found missing timestamps during "
                "candle aggregation."
            )



        df.sort_values(
            "timestamp",
            inplace=True
        )



        df.set_index(
            "timestamp",
            inplace=True
        )



        candles = (
            df.resample(
                timeframe,
                label="left",
                closed="left"
            )
            .agg(
                {
                    "open": "first",

                    "high": "max",

                    "low": "min",

                    "close": "last",

                    "volume": "sum",

                    "lastclose": "first"
                }
            )
        )



        before_cleanup = len(candles)



        candles.dropna(
            subset=[
                "open"
            ],
            inplace=True
        )



        removed = before_cleanup - len(candles)



        if removed > 0:

            logger.debug(
                f"Removed empty candles | "
                f"Count={removed}"
            )



        candles.reset_index(
            inplace=True
        )



        candles["volume"] = (
            candles["volume"]
            .fillna(0)
            .astype(int)
        )



        records = candles.to_dict(
            orient="records"
        )



        logger.info(
            f"Candle aggregation completed | "
            f"Timeframe={timeframe} | "
            f"Generated={len(records)}"
        )



        return records



    except Exception:


        logger.exception(
            f"Failed candle aggregation | "
            f"Timeframe={timeframe}"
        )


        raise