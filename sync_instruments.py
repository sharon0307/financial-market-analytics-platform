from market_analytics.extract.angel_master import (
    fetch_instruments
)

from market_analytics.database.repositories.instrument_repository import (
    upsert_instruments
)

from market_analytics.utils.logger import logger



def main():

    logger.info(
        "Starting instrument master sync"
    )


    try:

        data = fetch_instruments()


        logger.info(
            f"Total instruments downloaded: {len(data)}"
        )



        spot_equities = [
            x for x in data
            if x.get("exch_seg") in ["NSE", "BSE"]
            and x.get("symbol", "").endswith("-EQ")
        ]



        logger.info(
            f"Filtered spot equities: {len(spot_equities)}"
        )



        upsert_instruments(
            spot_equities
        )



        logger.info(
            "Instrument master sync completed successfully"
        )


    except Exception:

        logger.exception(
            "Instrument master sync failed"
        )

        raise



if __name__ == "__main__":

    main()