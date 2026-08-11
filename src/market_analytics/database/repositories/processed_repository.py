from sqlalchemy.dialects.postgresql import insert

from market_analytics.database.connection import SessionLocal
from market_analytics.database.models import ProcessedMarketData
from market_analytics.utils.logger import logger



def save_processed_market_data(records):

    session = SessionLocal()

    try:

        if not records:

            logger.warning(
                "No processed market data records received."
            )

            return 0


        logger.info(
            f"Saving processed market data | Records={len(records)}"
        )


        stmt = (
            insert(ProcessedMarketData)
            .values(records)
            .on_conflict_do_nothing(
                index_elements=[
                    "instrument_id",
                    "timestamp"
                ]
            )
        )


        result = session.execute(stmt)


        session.commit()


        logger.info(
            f"Processed market data saved | "
            f"Inserted={result.rowcount}"
        )


        return result.rowcount



    except Exception:

        session.rollback()

        logger.exception(
            "Failed saving processed market data"
        )

        raise



    finally:

        session.close()



def get_processed_data(
        instrument_id,
        start_time,
        end_time
):

    session = SessionLocal()

    try:

        logger.debug(
            f"Fetching processed data | "
            f"Instrument={instrument_id} | "
            f"From={start_time} | "
            f"To={end_time}"
        )


        data = (
            session.query(
                ProcessedMarketData
            )
            .filter(
                ProcessedMarketData.instrument_id == instrument_id,
                ProcessedMarketData.timestamp >= start_time,
                ProcessedMarketData.timestamp <= end_time
            )
            .order_by(
                ProcessedMarketData.timestamp
            )
            .all()
        )


        logger.debug(
            f"Processed data fetched | "
            f"Rows={len(data)}"
        )


        return data



    except Exception:

        logger.exception(
            "Fetching processed market data failed"
        )

        raise



    finally:

        session.close()




def get_previous_close(
        instrument_id,
        before_time
):

    session = SessionLocal()

    try:

        result = (
            session.query(
                ProcessedMarketData.close
            )
            .filter(
                ProcessedMarketData.instrument_id == instrument_id,
                ProcessedMarketData.timestamp < before_time
            )
            .order_by(
                ProcessedMarketData.timestamp.desc()
            )
            .first()
        )



        if result:

            logger.debug(
                f"Previous close found | "
                f"Instrument={instrument_id} | "
                f"Close={result[0]}"
            )


            return result[0]



        logger.warning(
            f"Previous close not found | "
            f"Instrument={instrument_id} | "
            f"Before={before_time}"
        )


        return None



    except Exception:

        logger.exception(
            f"Fetching previous close failed | "
            f"Instrument={instrument_id}"
        )

        raise



    finally:

        session.close()