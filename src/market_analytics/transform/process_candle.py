from market_analytics.database.repositories.processed_repository import (
    get_processed_data
)

from market_analytics.transform.candle_aggregation import (
    aggregate_candles
)

from market_analytics.database.repositories.candle_repository import (
    save_candles
)

from market_analytics.utils.logger import logger



def process_candles(
        instrument_id,
        start_time,
        end_time,
        timeframe,
        candle_model
):
    """
    Generate aggregated candles from processed 1m data.
    """


    logger.info(
        f"Starting candle processing | "
        f"Instrument={instrument_id} | "
        f"Timeframe={timeframe} | "
        f"Table={candle_model.__tablename__}"
    )


    try:

        # ---------------------------------
        # 1. Fetch processed 1 minute data
        # ---------------------------------

        processed_data = get_processed_data(
            instrument_id,
            start_time,
            end_time
        )


        logger.info(
            f"Processed 1m rows fetched: {len(processed_data)} | "
            f"Instrument={instrument_id}"
        )


        if not processed_data:

            logger.warning(
                f"No processed data found. "
                f"Skipping candle generation | "
                f"Instrument={instrument_id} | "
                f"Timeframe={timeframe}"
            )

            return 0



        # ---------------------------------
        # 2. Aggregate candles
        # ---------------------------------

        candles = aggregate_candles(
            processed_data,
            timeframe
        )


        logger.info(
            f"Generated candles: {len(candles)} | "
            f"Timeframe={timeframe}"
        )



        # Add instrument_id

        for candle in candles:

            candle["instrument_id"] = instrument_id



        # ---------------------------------
        # 3. Save candles
        # ---------------------------------

        inserted = save_candles(
            candle_model,
            candles
        )


        logger.info(
            f"Candle processing completed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe} | "
            f"Inserted={inserted}"
        )


        return inserted



    except Exception:

        logger.exception(
            f"Failed candle processing | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe}"
        )

        raise