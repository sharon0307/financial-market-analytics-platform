import requests

from market_analytics.utils.logger import logger


MASTER_URL = (
    "https://margincalculator.angelone.in/"
    "OpenAPI_File/files/OpenAPIScripMaster.json"
)


def fetch_instruments():

    logger.info(
        "Downloading Angel One instrument master."
    )

    try:

        response = requests.get(
            MASTER_URL,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        logger.info(
            f"Successfully downloaded {len(data)} instruments."
        )

        return data

    except Exception:

        logger.exception(
            "Failed to download Angel One instrument master."
        )

        raise