from datetime import datetime

from market_analytics.database.repositories.instrument_repository import (
    get_by_token
)

from market_analytics.extract.historical_downloader import (
    HistoricalDownloader
)

from market_analytics.extract.raw_loader import (
    parse_candle_data
)

from market_analytics.database.repositories.raw_repository import (
    save_raw_payload,
    save_raw_market_data
)

from market_analytics.utils.logger import logger



def run(
        instrument_id,
        start_date,
        end_date
):

    logger.info(
        f"Starting historical download job | "
        f"Instrument={instrument_id} | "
        f"From={start_date} | "
        f"To={end_date}"
    )


    try:

        downloader = HistoricalDownloader()


        # ---------------------------------
        # Get instrument details
        # ---------------------------------

        instrument = get_by_token(
            instrument_id
        )


        if instrument is None:

            raise Exception(
                f"Instrument not found: {instrument_id}"
            )


        logger.info(
            f"Instrument found | "
            f"Symbol={instrument.symbol} | "
            f"Exchange={instrument.exchange} | "
            f"Token={instrument.token}"
        )


        start_time = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )


        end_time = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        )


        # ---------------------------------
        # Download from SmartAPI
        # ---------------------------------

        response = downloader.download(

            exchange=instrument.exchange,

            token=instrument.token,

            interval="ONE_MINUTE",

            start_time=start_time,

            end_time=end_time

        )


        candles = response.get(
            "data",
            []
        )


        logger.info(
            f"Download completed | "
            f"Candles={len(candles)}"
        )


        if not candles:

            logger.warning(
                "No candle data received."
            )

            return



        # ---------------------------------
        # Save complete broker response
        # ---------------------------------

        payload_id = save_raw_payload(

            instrument_id=instrument.id,

            source="ANGEL",

            interval="ONE_MINUTE",

            request_from=start_time,

            request_to=end_time,

            payload=response

        )


        logger.info(
            f"Raw payload saved | "
            f"PayloadID={payload_id}"
        )



        # ---------------------------------
        # Convert to raw market format
        # ---------------------------------

        records = parse_candle_data(

            instrument_id=instrument.id,

            payload_id=payload_id,

            data=candles

        )


        logger.info(
            f"Parsed raw market data | "
            f"Records={len(records)}"
        )



        save_raw_market_data(
            records
        )


        logger.info(
            "Historical download job completed successfully."
        )



    except Exception:


        logger.exception(
            "Historical download job failed."
        )

        raise




if __name__ == "__main__":


    import argparse


    parser = argparse.ArgumentParser(
        description="Download historical market data"
    )


    parser.add_argument(
        "--instrument-id",
        required=True,
        type=int
    )


    parser.add_argument(
        "--start-date",
        required=True
    )


    parser.add_argument(
        "--end-date",
        required=True
    )


    args = parser.parse_args()



    run(

        instrument_id=args.instrument_id,

        start_date=args.start_date,

        end_date=args.end_date

    )