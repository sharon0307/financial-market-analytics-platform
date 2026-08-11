from market_analytics.transform.analytics_processor import (
    process_indicator
)

from market_analytics.analytics.returns import (
    calculate_returns
)

from market_analytics.database.models import (
    Candle2M,
    Candle3M,
    Candle5M,
    Candle15M
)

from market_analytics.utils.logger import logger



TIMEFRAME_MODELS = {

    "2m": Candle2M,

    "3m": Candle3M,

    "5m": Candle5M,

    "15m": Candle15M

}



def process_returns(
        instrument_id,
        timeframe,
        start_time,
        end_time
):

    logger.info(
        f"Starting returns processing | "
        f"Instrument={instrument_id} | "
        f"Timeframe={timeframe} | "
        f"From={start_time} | "
        f"To={end_time}"
    )


    try:

        candle_model = TIMEFRAME_MODELS.get(
            timeframe
        )

        logger.debug(
            f"Using candle model: {candle_model.__tablename__}"
        )

        if candle_model is None:

            logger.error(
                f"Unsupported timeframe | "
                f"Timeframe={timeframe}"
            )

            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )



        result = process_indicator(

            candle_model=candle_model,

            timeframe=timeframe,

            instrument_id=instrument_id,

            start_time=start_time,

            end_time=end_time,

            indicator_function=calculate_returns
        )


        logger.info(
            f"Returns processing completed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe} | "
            f"Inserted={result}"
        )


        return result



    except Exception:

        logger.exception(
            f"Returns processing failed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe}"
        )

        raise