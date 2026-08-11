from datetime import timedelta

from market_analytics.extract.smartapi_client import SmartAPIClient
from market_analytics.utils.logger import logger


class HistoricalDownloader:

    MAX_DAYS_PER_REQUEST = 30

    def __init__(self):
        self.client = SmartAPIClient()

    def _generate_chunks(
        self,
        start_time,
        end_time
    ):
        """
        Generate deterministic, non-overlapping logical
        30-day chunks.

        Example:

            Jan 1 -> Jan 31
            Jan 31 -> Mar 2
            Mar 2 -> Apr 1

        No minute adjustment is applied between chunks.
        """

        chunks = []

        current_start = start_time

        while current_start < end_time:

            current_end = (
                current_start
                + timedelta(days=self.MAX_DAYS_PER_REQUEST)
            )

            if current_end > end_time:
                current_end = end_time

            chunks.append(
                (
                    current_start,
                    current_end
                )
            )

            # Next chunk starts exactly at the
            # previous chunk's logical boundary.
            current_start = current_end

        return chunks

    def download(
        self,
        exchange,
        token,
        interval,
        start_time,
        end_time
    ):
        """
        Download historical market data chunk-by-chunk.

        Each yielded result represents one SmartAPI request.

        The downloader is responsible for:
            - authentication
            - 30-day chunking
            - SmartAPI requests
            - returning raw responses

        Database persistence and duplicate handling are
        intentionally handled outside this class.
        """

        logger.info(
            f"Starting historical download | "
            f"Exchange={exchange} | "
            f"Token={token} | "
            f"Interval={interval} | "
            f"From={start_time} | "
            f"To={end_time}"
        )

        try:

            # --------------------------------------------------
            # Ensure SmartAPI session exists
            # --------------------------------------------------

            if self.client.smart_api is None:

                logger.info(
                    "SmartAPI session not found. Logging in."
                )

                self.client.login()

            # --------------------------------------------------
            # Generate deterministic chunks
            # --------------------------------------------------

            chunks = self._generate_chunks(
                start_time,
                end_time
            )

            logger.info(
                f"Total download chunks created: {len(chunks)}"
            )

            # --------------------------------------------------
            # Download each chunk
            # --------------------------------------------------

            for index, (chunk_start, chunk_end) in enumerate(
                chunks,
                start=1
            ):

                logger.info(
                    f"Downloading chunk {index}/{len(chunks)} | "
                    f"From={chunk_start} | "
                    f"To={chunk_end}"
                )

                params = {
                    "exchange": exchange,
                    "symboltoken": token,
                    "interval": interval,
                    "fromdate": chunk_start.strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "todate": chunk_end.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }

                logger.info(
                    f"SmartAPI request parameters: {params}"
                )

                response = self.client.smart_api.getCandleData(
                    params
                )

                # --------------------------------------------------
                # Validate response
                # --------------------------------------------------

                if not response.get("status"):

                    message = response.get(
                        "message",
                        "Unknown SmartAPI error"
                    )

                    logger.error(
                        f"Chunk failed | "
                        f"Chunk={index} | "
                        f"Message={message}"
                    )

                    raise Exception(message)

                candles = response.get(
                    "data",
                    []
                ) or []

                logger.info(
                    f"Chunk completed | "
                    f"Chunk={index}/{len(chunks)} | "
                    f"Candles received={len(candles)}"
                )

                # --------------------------------------------------
                # Return raw chunk immediately
                # --------------------------------------------------

                yield {
                    "chunk_number": index,
                    "total_chunks": len(chunks),
                    "start_time": chunk_start,
                    "end_time": chunk_end,
                    "response": response,
                    "data": candles
                }

            logger.info(
                "Historical download completed successfully."
            )

        except Exception:

            logger.exception(
                "Historical download failed."
            )

            raise