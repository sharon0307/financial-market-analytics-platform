from market_analytics.utils.logger import logger


def calculate_returns(candles):

    """
    Calculate candle returns.

    First candle uses lastclose
    from processed candle data.
    """


    if not candles:

        logger.warning(
            "Returns calculation skipped | No candles received"
        )

        return []


    logger.info(
        f"Returns calculation started | Candles={len(candles)}"
    )


    results = []


    previous_close = None

    calculated = 0



    for candle in candles:


        # First candle of dataset/day
        if previous_close is None:


            previous_close = candle.lastclose



        if previous_close:


            return_pct = round(
                (
                    (
                        candle.close -
                        previous_close
                    )
                    /
                    previous_close
                )
                *
                100,
                4
            )

            calculated += 1


        else:


            return_pct = None


            logger.warning(
                f"Missing previous close | "
                f"Timestamp={candle.timestamp}"
            )



        results.append(
            {
                "timestamp": candle.timestamp,

                "values": {

                    "return_pct": return_pct

                }
            }
        )


        previous_close = candle.close



    logger.info(
        f"Returns calculation completed | "
        f"Rows={len(results)} | "
        f"Calculated={calculated}"
    )


    return results