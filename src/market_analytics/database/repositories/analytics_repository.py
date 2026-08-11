from sqlalchemy.dialects.postgresql import insert

from market_analytics.database.connection import SessionLocal
from market_analytics.database.models import CandleAnalytics
from market_analytics.utils.logger import logger



def save_candle_analytics(records):

    session = SessionLocal()

    try:

        if not records:

            logger.warning(
                "No candle analytics records received for saving."
            )

            return 0


        logger.info(
            f"Saving candle analytics records | "
            f"Count={len(records)} | "
            f"Columns={list(records[0].keys())}"
        )


        stmt = insert(
            CandleAnalytics
        ).values(records)


        update_columns = {
            key
            for record in records
            for key in record.keys()
            if key not in [
                "id",
                "instrument_id",
                "timestamp",
                "timeframe",
                "created_at"
            ]
        }

        if not update_columns:

            logger.warning(
                "No update columns found for candle analytics."
            )

            session.rollback()

            return 0


        stmt = stmt.on_conflict_do_update(
            index_elements=[
                "instrument_id",
                "timestamp",
                "timeframe"
            ],
            set_={
                column: getattr(stmt.excluded, column)
                for column in update_columns
            }
        )


        result = session.execute(stmt)

        session.commit()


        logger.info(
            f"Candle analytics saved successfully. "
            f"Inserted/Updated rows: {result.rowcount}"
        )


        return result.rowcount


    except Exception:

        session.rollback()

        logger.exception(
            "Failed to save candle analytics."
        )

        raise


    finally:

        session.close()