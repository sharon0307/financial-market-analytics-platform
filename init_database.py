from market_analytics.database.connection import engine, Base
from market_analytics.database import models

from market_analytics.utils.logger import logger



def create_tables():

    logger.info(
        "Starting database table creation..."
    )


    try:

        Base.metadata.create_all(
            engine
        )


        logger.info(
            "Database tables created successfully."
        )


    except Exception:

        logger.exception(
            "Failed creating database tables."
        )

        raise



if __name__ == "__main__":

    create_tables()