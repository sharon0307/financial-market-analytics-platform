from sqlalchemy.dialects.postgresql import insert

from market_analytics.database.connection import SessionLocal
from market_analytics.utils.logger import logger



def save_candles(
        candle_model,
        records
):
    """
    Generic candle insert.

    candle_model:
        Candle2M / Candle3M / Candle5M / Candle15M

    records:
        list of candle dictionaries
    """


    if not records:

        logger.warning(
            "No candle records received for saving."
        )

        return 0



    table_name = candle_model.__tablename__



    required_fields = [
        "instrument_id",
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]



    missing_fields = [
        field
        for field in required_fields
        if field not in records[0]
    ]



    if missing_fields:

        logger.error(
            f"Invalid candle records | "
            f"Table={table_name} | "
            f"MissingFields={missing_fields}"
        )

        raise ValueError(
            f"Missing candle fields: {missing_fields}"
        )



    session = SessionLocal()



    try:


        logger.info(
            f"Saving candles | "
            f"Table={table_name} | "
            f"Records={len(records)}"
        )



        stmt = insert(
            candle_model
        ).values(
            records
        )



        logger.debug(
            f"Conflict handling enabled | "
            f"Keys=instrument_id,timestamp"
        )



        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                "instrument_id",
                "timestamp"
            ]
        )



        result = session.execute(
            stmt
        )



        session.commit()



        logger.info(
            f"Candle save completed | "
            f"Table={table_name} | "
            f"Inserted={result.rowcount}"
        )



        return result.rowcount



    except Exception:


        session.rollback()



        logger.exception(
            f"Failed saving candles | "
            f"Table={table_name}"
        )


        raise



    finally:


        session.close()





def get_candles(
        candle_model,
        instrument_id,
        start_time,
        end_time
):
    """
    Generic candle fetch.
    """


    table_name = candle_model.__tablename__


    session = SessionLocal()



    try:


        logger.info(
            f"Fetching candles | "
            f"Table={table_name} | "
            f"Instrument={instrument_id} | "
            f"Range={start_time} -> {end_time}"
        )



        candles = (
            session.query(
                candle_model
            )
            .filter(

                candle_model.instrument_id == instrument_id,

                candle_model.timestamp >= start_time,

                candle_model.timestamp <= end_time

            )
            .order_by(
                candle_model.timestamp
            )
            .all()
        )



        logger.info(
            f"Candle fetch completed | "
            f"Table={table_name} | "
            f"Rows={len(candles)}"
        )



        return candles



    except Exception:


        logger.exception(
            f"Failed fetching candles | "
            f"Table={table_name} | "
            f"Instrument={instrument_id}"
        )


        raise



    finally:


        session.close()