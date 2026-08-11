from sqlalchemy.dialects.postgresql import insert

from market_analytics.database.connection import SessionLocal
from market_analytics.database.models import (
    RawMarketPayload,
    RawMarketData
)
from market_analytics.utils.logger import logger



def save_raw_payload(
        instrument_id,
        source,
        interval,
        request_from,
        request_to,
        payload
):
    """
    Stores the complete broker response.
    This should never be modified after insertion.
    """

    session = SessionLocal()

    try:

        logger.info(
            f"Saving raw payload | "
            f"Instrument={instrument_id} | "
            f"Source={source} | "
            f"Interval={interval}"
        )


        record = RawMarketPayload(
            instrument_id=instrument_id,
            source=source,
            interval=interval,
            request_from=request_from,
            request_to=request_to,
            payload=payload
        )

        session.add(record)

        session.commit()

        session.refresh(record)


        logger.info(
            f"Raw payload saved successfully. "
            f"Payload ID={record.id}"
        )


        return record.id


    except Exception:

        session.rollback()

        logger.exception(
            "Failed saving raw market payload."
        )

        raise


    finally:

        session.close()




def save_raw_market_data(records):

    session = SessionLocal()

    try:

        if not records:

            logger.warning(
                "No raw market data records received."
            )

            return 0


        logger.info(
            f"Saving {len(records)} raw market data records."
        )


        stmt = insert(
            RawMarketData
        ).values(records)


        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                "instrument_id",
                "timestamp"
            ]
        )


        result = session.execute(stmt)

        session.commit()


        logger.info(
            f"Raw market data saved. "
            f"Inserted rows={result.rowcount}"
        )


        return result.rowcount


    except Exception:

        session.rollback()

        logger.exception(
            "Failed saving raw market data."
        )

        raise


    finally:

        session.close()


def get_raw_market_data(
        instrument_id,
        start_time,
        end_time
):
    """
    Fetch raw 1-minute OHLCV data
    for processing.
    """

    session = SessionLocal()

    try:

        logger.info(
            f"Fetching raw 1 minute data | "
            f"Instrument={instrument_id}"
        )


        data = (
            session.query(
                RawMarketData
            )
            .filter(
                RawMarketData.instrument_id == instrument_id,
                RawMarketData.timestamp >= start_time,
                RawMarketData.timestamp <= end_time
            )
            .order_by(
                RawMarketData.timestamp
            )
            .all()
        )


        logger.info(
            f"Fetched {len(data)} raw processing rows."
        )


        return data


    except Exception:

        logger.exception(
            "Failed fetching raw market data for processing."
        )

        raise


    finally:

        session.close()




def get_raw_payload(
        payload_id
):
    """
    Fetch original SmartAPI response.
    Used for debugging/reprocessing.
    """

    session = SessionLocal()

    try:

        logger.info(
            f"Fetching raw payload. Payload ID={payload_id}"
        )


        payload = (
            session.query(
                RawMarketPayload
            )
            .filter(
                RawMarketPayload.id == payload_id
            )
            .first()
        )


        if payload:

            logger.info(
                f"Raw payload found. Payload ID={payload_id}"
            )

        else:

            logger.warning(
                f"Raw payload not found. Payload ID={payload_id}"
            )


        return payload


    except Exception:

        logger.exception(
            "Failed fetching raw payload."
        )

        raise


    finally:

        session.close()