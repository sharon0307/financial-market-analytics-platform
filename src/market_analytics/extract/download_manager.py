from market_analytics.extract.historical_downloader import (
    HistoricalDownloader
)

from market_analytics.extract.raw_loader import (
    parse_candle_data
)

from market_analytics.database.repositories.raw_repository import (
    save_raw_payload,
    save_raw_market_data
)

from market_analytics.utils.logger import logger


class DownloadManager:

    def __init__(self):

        self.downloader = HistoricalDownloader()

    def download_instrument(
        self,
        instrument_id,
        exchange,
        token,
        interval,
        start_time,
        end_time
    ):
        """
        Download historical data for one instrument.

        Pipeline:

            HistoricalDownloader
                    ↓
            raw_market_payloads
                    ↓
            raw_market_data

        The original broker response is stored before
        parsing the individual candles.
        """

        logger.info(
            f"Starting download manager | "
            f"Instrument={instrument_id} | "
            f"Exchange={exchange} | "
            f"Token={token} | "
            f"Interval={interval}"
        )

        total_payloads = 0
        total_raw_rows = 0

        try:

            for chunk in self.downloader.download(
                exchange=exchange,
                token=token,
                interval=interval,
                start_time=start_time,
                end_time=end_time
            ):

                chunk_number = chunk["chunk_number"]
                total_chunks = chunk["total_chunks"]

                chunk_start = chunk["start_time"]
                chunk_end = chunk["end_time"]

                response = chunk["response"]
                candles = chunk["data"]

                logger.info(
                    f"Processing downloaded chunk | "
                    f"Chunk={chunk_number}/{total_chunks} | "
                    f"Candles={len(candles)}"
                )

                # --------------------------------------------------
                # 1. Save original SmartAPI response
                # --------------------------------------------------

                payload_id = save_raw_payload(
                    instrument_id=instrument_id,
                    source="SMARTAPI",
                    interval=interval,
                    request_from=chunk_start,
                    request_to=chunk_end,
                    payload=response
                )

                total_payloads += 1

                logger.info(
                    f"Raw payload stored | "
                    f"Payload ID={payload_id}"
                )

                # --------------------------------------------------
                # 2. Parse candle response
                # --------------------------------------------------

                records = parse_candle_data(
                    instrument_id=instrument_id,
                    payload_id=payload_id,
                    data=candles
                )

                logger.info(
                    f"Parsed raw candle records | "
                    f"Records={len(records)}"
                )

                # --------------------------------------------------
                # 3. Save raw market data
                # --------------------------------------------------

                inserted = save_raw_market_data(
                    records
                )

                total_raw_rows += inserted

                logger.info(
                    f"Raw market data saved | "
                    f"Chunk={chunk_number}/{total_chunks} | "
                    f"Inserted={inserted}"
                )

            logger.info(
                f"Download manager completed | "
                f"Instrument={instrument_id} | "
                f"Payloads={total_payloads} | "
                f"Raw rows inserted={total_raw_rows}"
            )

            return {
                "instrument_id": instrument_id,
                "payloads": total_payloads,
                "raw_rows_inserted": total_raw_rows
            }

        except Exception:

            logger.exception(
                f"Download manager failed | "
                f"Instrument={instrument_id}"
            )

            raise