from pathlib import Path
import sys


# Add src directory to Python path
sys.path.append(
    str(Path(__file__).parent / "src")
)


from market_analytics.utils.logger import logger



def main():

    logger.info(
        "Financial Market Analytics Platform Started"
    )


    try:

        # Application startup logic
        # Add pipeline execution here later

        logger.info(
            "Application initialized successfully"
        )


    except Exception:

        logger.exception(
            "Application startup failed"
        )

        raise



if __name__ == "__main__":

    main()