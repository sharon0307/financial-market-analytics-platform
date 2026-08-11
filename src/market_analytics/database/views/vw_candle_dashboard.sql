CREATE OR REPLACE VIEW vw_candle_dashboard AS

SELECT
    c.instrument_id,
    i.symbol,

    c.timestamp,
    c.open,
    c.high,
    c.low,
    c.close,
    c.volume,
    c.lastclose,

    a.timeframe,
    a.return_pct,
    a.vwap

FROM candles_5m c

LEFT JOIN candle_analytics a
    ON c.instrument_id = a.instrument_id
    AND c.timestamp = a.timestamp
    AND a.timeframe = '5m'

LEFT JOIN instruments i
    ON c.instrument_id = i.id;