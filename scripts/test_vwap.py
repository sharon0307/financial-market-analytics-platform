from datetime import datetime

from market_analytics.transform.process_vwap import (
    process_vwap
)

from market_analytics.utils.logger import logger



def run():

    instrument_id = 186

    timeframe = "5m"


    start_time = datetime(
        2026,
        8,
        4,
        9,
        15
    )


    end_time = datetime(
        2026,
        8,
        5,
        15,
        29
    )


    logger.info(
        f"Starting VWAP test | "
        f"Instrument={instrument_id} | "
        f"Timeframe={timeframe} | "
        f"From={start_time} | "
        f"To={end_time}"
    )


    try:

        inserted = process_vwap(
            instrument_id=instrument_id,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time
        )


        logger.info(
            f"VWAP test completed | "
            f"Inserted={inserted}"
        )


        return inserted



    except Exception:


        logger.exception(
            f"VWAP test failed | "
            f"Instrument={instrument_id}"
        )

        raise




if __name__ == "__main__":

    run()