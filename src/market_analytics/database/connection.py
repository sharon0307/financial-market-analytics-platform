from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from market_analytics.utils.config import config
from market_analytics.utils.logger import logger


logger.info(
    "Initializing database engine."
)


try:

    engine = create_engine(
        config.DATABASE_URL,
        echo=False
    )

    logger.info(
        "Database engine initialized successfully."
    )


except Exception:

    logger.exception(
        "Failed to initialize database engine."
    )

    raise



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()



def get_connection():

    logger.info(
        "Opening database connection."
    )

    try:

        connection = engine.connect()

        logger.info(
            "Database connection established."
        )

        return connection


    except Exception:

        logger.exception(
            "Failed to establish database connection."
        )

        raise