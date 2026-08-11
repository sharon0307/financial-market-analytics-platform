# Financial Market Analytics Platform

A Python-based financial market data pipeline for downloading historical 1-minute market data, processing OHLCV data, generating candles, calculating returns/VWAP, and serving data to Power BI.

## Architecture

```text
SmartAPI
   ↓
Historical Downloader
   ↓
Raw Payloads
   ↓
Raw Market Data
   ↓
1-Minute Processing
   ↓
Candle Aggregation (2m / 5m / ...)
   ↓
Returns + VWAP
   ↓
PostgreSQL Dashboard View
   ↓
Power BI
```

## Tech Stack

- Python 3.13
- PostgreSQL
- SQLAlchemy
- Pandas
- Angel One SmartAPI
- Power BI

## Main Components

```text
src/market_analytics/
├── database/
├── extract/
├── transform/
└── utils/

scripts/
database/
├── views/
docs/
powerbi/
```

### Data Flow

1. Download historical data from SmartAPI.
2. Store the original API response in `raw_market_payloads`.
3. Parse candles into `raw_market_data`.
4. Process 1-minute data into `processed_market_data`.
5. Generate timeframe candles such as 2m and 5m.
6. Calculate returns and VWAP.
7. Expose dashboard data through PostgreSQL views.
8. Connect Power BI to the dashboard view.

## Running the Pipeline

Example:

```powershell
python .\scriptsun_pipeline.py `
    --instruments 835 2052 `
    --start 2026-08-06 `
    --end 2026-08-10
```

Where:

- `835` = TCS-EQ
- `2052` = RELIANCE-EQ

The instrument ID is the internal database ID. The SmartAPI token is stored separately in the instrument master.

## Database

The main tables include:

- `instruments`
- `raw_market_payloads`
- `raw_market_data`
- `processed_market_data`
- `candles_2m`
- `candles_5m`
- `candle_analytics`

Dashboard view:

```text
vw_candle_dashboard
```

## Power BI

The dashboard currently uses:

- Latest Price
- Previous Close
- Return %
- VWAP
- Price trend
- Price vs VWAP
- Return trend
- Symbol/date filters

Recommended DAX measures:

```DAX
Latest Price =
MAX(vw_candle_dashboard[close])
```

```DAX
Previous Close =
MAX(vw_candle_dashboard[lastclose])
```

```DAX
Return % =
MAX(vw_candle_dashboard[return_pct])
```

```DAX
VWAP =
MAX(vw_candle_dashboard[vwap])
```

## Environment

Create a local `.env` containing SmartAPI and PostgreSQL credentials.

Never commit `.env` or API credentials to GitHub.

See `GITHUB_SETUP.md` for repository creation, Git commands, `.gitignore`, and pushing the project to GitHub.

## Current Status

Implemented and tested:

- SmartAPI authentication
- Historical 1-minute download
- Raw data ingestion
- Multi-day processing
- Multi-instrument processing
- Missing-minute handling
- Previous-close handling
- Candle aggregation
- Returns
- VWAP
- PostgreSQL dashboard view
- Power BI dashboard
