from sqlalchemy.dialects.postgresql import insert

from market_analytics.database.connection import SessionLocal
from market_analytics.database.models import Instrument
from market_analytics.utils.logger import logger



def upsert_instruments(data):

    session = SessionLocal()

    try:

        logger.info(
            f"Starting instrument sync | Received={len(data)}"
        )


        records = []

        for item in data:

            records.append(
                {
                    "token": item["token"],
                    "symbol": item["symbol"],
                    "name": item["name"],
                    "exchange": item["exch_seg"],
                    "instrument_type": "EQUITY",
                    "lot_size": int(item["lotsize"]),
                    "tick_size": item["tick_size"],
                }
            )


        stmt = insert(
            Instrument
        ).values(
            records
        )


        stmt = stmt.on_conflict_do_update(
            index_elements=["token"],
            set_={
                "symbol": stmt.excluded.symbol,
                "name": stmt.excluded.name,
                "exchange": stmt.excluded.exchange,
                "lot_size": stmt.excluded.lot_size,
                "tick_size": stmt.excluded.tick_size,
            }
        )


        result = session.execute(
            stmt
        )


        session.commit()


        logger.info(
            f"Instrument sync completed | "
            f"Records={len(records)} | "
            f"DB Rows={result.rowcount}"
        )


        return len(records)



    except Exception:

        session.rollback()

        logger.exception(
            "Instrument sync failed"
        )

        raise



    finally:

        session.close()




def get_all_instruments():

    session = SessionLocal()

    try:

        instruments = (
            session.query(Instrument)
            .all()
        )


        logger.debug(
            f"Fetched instruments | Count={len(instruments)}"
        )


        return instruments



    except Exception:

        logger.exception(
            "Fetching all instruments failed"
        )

        raise



    finally:

        session.close()




def get_by_symbol(symbol):

    session = SessionLocal()

    try:

        instrument = (
            session.query(Instrument)
            .filter(
                Instrument.symbol == symbol.upper()
            )
            .first()
        )


        if instrument:

            logger.debug(
                f"Instrument found | Symbol={symbol}"
            )

        else:

            logger.warning(
                f"Instrument not found | Symbol={symbol}"
            )


        return instrument



    except Exception:

        logger.exception(
            f"Fetching instrument failed | Symbol={symbol}"
        )

        raise



    finally:

        session.close()




def get_by_token(token):

    session = SessionLocal()

    try:

        instrument = (
            session.query(Instrument)
            .filter(
                Instrument.token == str(token)
            )
            .first()
        )


        if instrument:

            logger.debug(
                f"Instrument found | Token={token}"
            )

        else:

            logger.warning(
                f"Instrument not found | Token={token}"
            )


        return instrument



    except Exception:

        logger.exception(
            f"Fetching instrument failed | Token={token}"
        )

        raise



    finally:

        session.close()




def get_spot_equities():

    session = SessionLocal()

    try:

        instruments = (
            session.query(Instrument)
            .filter(
                Instrument.exchange.in_(
                    ["NSE", "BSE"]
                )
            )
            .order_by(
                Instrument.name
            )
            .all()
        )


        logger.info(
            f"Fetched spot equities | Count={len(instruments)}"
        )


        return instruments



    except Exception:

        logger.exception(
            "Fetching spot equities failed"
        )

        raise



    finally:

        session.close()