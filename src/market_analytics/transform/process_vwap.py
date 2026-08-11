from market_analytics.transform.analytics_processor import (
    process_indicator
)

from market_analytics.analytics.vwap import (
    calculate_vwap
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



def process_vwap(
        instrument_id,
        timeframe,
        start_time,
        end_time
):

    logger.info(
        f"Starting VWAP processing | "
        f"Instrument={instrument_id} | "
        f"Timeframe={timeframe}"
    )


    try:

        candle_model = TIMEFRAME_MODELS.get(
            timeframe
        )


        if candle_model is None:

            logger.error(
                f"Unsupported timeframe for VWAP | "
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

            indicator_function=calculate_vwap
        )


        logger.info(
            f"VWAP processing completed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe} | "
            f"Inserted={result}"
        )


        return result



    except Exception:

        logger.exception(
            f"VWAP processing failed | "
            f"Instrument={instrument_id} | "
            f"Timeframe={timeframe}"
        )

        raise