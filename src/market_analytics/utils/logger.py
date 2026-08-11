import logging
import sys

from pathlib import Path
from datetime import datetime



logger = logging.getLogger(
    "market_analytics"
)


logger.setLevel(
    logging.INFO
)



def setup_logger():

    if logger.handlers:
        return logger



    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )



    # Project root
    project_root = Path(
        __file__
    ).resolve().parents[3]


    base_log_dir = (
        project_root / "logs"
    )


    base_log_dir.mkdir(
        exist_ok=True
    )



    # -----------------------------
    # Console
    # -----------------------------

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )



    # -----------------------------
    # Master log
    # -----------------------------

    master_log = logging.FileHandler(
        base_log_dir / "market_analytics.log",
        encoding="utf-8"
    )

    master_log.setFormatter(
        formatter
    )

    logger.addHandler(
        master_log
    )



    # -----------------------------
    # Run log
    # -----------------------------

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    today_dir = (
        base_log_dir / today
    )


    today_dir.mkdir(
        exist_ok=True
    )


    run_file = (
        datetime.now().strftime(
            "%H-%M-%S-%f"
        )
        + ".log"
    )



    run_log = logging.FileHandler(
        today_dir / run_file,
        encoding="utf-8"
    )


    run_log.setFormatter(
        formatter
    )


    logger.addHandler(
        run_log
    )


    return logger



logger = setup_logger()