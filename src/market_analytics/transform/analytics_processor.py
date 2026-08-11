from market_analytics.database.repositories.candle_repository import (
    get_candles
)

from market_analytics.database.repositories.analytics_repository import (
    save_candle_analytics
)

from market_analytics.utils.logger import logger



def process_indicator(
        candle_model,
        timeframe,
        instrument_id,
        start_time,
        end_time,
        indicator_function
):

    indicator_name = indicator_function.__name__


    logger.info(
        f"Starting analytics processing | "
        f"Indicator={indicator_name} | "
        f"Timeframe={timeframe} | "
        f"Instrument={instrument_id} | "
        f"CandleTable={candle_model.__tablename__}"
    )


    try:

        # 1. Fetch candles

        candles = get_candles(
            candle_model,
            instrument_id,
            start_time,
            end_time
        )


        logger.info(
            f"Candles fetched: {len(candles)} | "
            f"Timeframe={timeframe}"
        )


        if not candles:

            logger.warning(
                f"No candles found. "
                f"Skipping {indicator_name} calculation."
            )

            return 0



        # 2. Calculate indicator

        indicator_results = indicator_function(
            candles
        )

        if not indicator_results:

            logger.warning(
                f"No indicator results generated | "
                f"Indicator={indicator_name}"
            )

            return 0

        logger.info(
            f"Indicator calculation completed | "
            f"Indicator={indicator_name} | "
            f"Results={len(indicator_results)}"
        )



        # 3. Convert to database records

        records = []


        for result in indicator_results:

            records.append(
                {
                    "instrument_id": instrument_id,

                    "timestamp": result["timestamp"],

                    "timeframe": timeframe,

                    **result["values"]
                }
            )



        logger.info(
            f"Prepared {len(records)} analytics records "
            f"for database."
        )



        # 4. Save

        inserted = save_candle_analytics(
            records
        )


        logger.info(
            f"Analytics processing completed | "
            f"Indicator={indicator_name} | "
            f"Inserted/Updated={inserted}"
        )


        return inserted


    except Exception:

        logger.exception(
            f"Failed processing analytics | "
            f"Indicator={indicator_name} | "
            f"Instrument={instrument_id}"
        )

        raise