from market_analytics.utils.logger import logger


def calculate_vwap(candles):

    """
    Calculate intraday VWAP.

    VWAP resets every trading day.
    """


    if not candles:

        logger.warning(
            "VWAP calculation skipped | No candles received"
        )

        return []


    logger.info(
        f"VWAP calculation started | Candles={len(candles)}"
    )


    results = []


    daily_volume = 0
    daily_value = 0

    current_day = None

    reset_count = 0


    for candle in candles:


        candle_day = candle.timestamp.date()


        # New trading day reset
        if current_day != candle_day:


            current_day = candle_day

            daily_volume = 0
            daily_value = 0

            reset_count += 1


            logger.debug(
                f"VWAP reset | Date={candle_day}"
            )



        typical_price = (
            candle.high +
            candle.low +
            candle.close
        ) / 3



        daily_value += (
            typical_price *
            candle.volume
        )


        daily_volume += candle.volume



        if daily_volume > 0:


            vwap = (
                daily_value /
                daily_volume
            )


        else:


            vwap = None


            logger.warning(
                f"VWAP volume zero | "
                f"Timestamp={candle.timestamp}"
            )



        results.append(
            {
                "timestamp": candle.timestamp,

                "values": {
                    "vwap": round(vwap, 4)
                    if vwap is not None
                    else None
                }
            }
        )



    logger.info(
        f"VWAP calculation completed | "
        f"Rows={len(results)} | "
        f"Daily resets={reset_count}"
    )


    return results