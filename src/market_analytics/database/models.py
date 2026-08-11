from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    BigInteger,
    Text
)

from sqlalchemy.dialects.postgresql import JSONB
from market_analytics.database.connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (func, UniqueConstraint)

class Instrument(Base):

    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True)

    token = Column(
        String(50),
        unique=True,
        nullable=False
    )

    symbol = Column(
        String(100),
        nullable=False
    )

    name = Column(String(200))

    exchange = Column(String(20))

    instrument_type = Column(String(50))

    lot_size = Column(Integer)

    tick_size = Column(String(20))

    
    def __repr__(self):
        return (
            f"Instrument("
            f"symbol='{self.symbol}', "
            f"token='{self.token}', "
            f"exchange='{self.exchange}')"
        )

    raw_payloads = relationship(
        "RawMarketPayload",
        back_populates="instrument"
    )

    raw_data = relationship(
        "RawMarketData",
        back_populates="instrument"
    )


class RawMarketPayload(Base):

    __tablename__ = "raw_market_payloads"

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    source = Column(
        String(50),
        nullable=False
    )

    interval = Column(
        String(20)
    )

    request_from = Column(
        DateTime
    )

    request_to = Column(
        DateTime
    )

    payload = Column(
        JSONB
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    instrument = relationship(
        "Instrument",
        back_populates="raw_payloads"
    )

    market_data = relationship(
        "RawMarketData",
        back_populates="payload"
    )


class RawMarketData(Base):

    __tablename__ = "raw_market_data"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_raw_market_instrument_timestamp"
        ),

    )


    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(Float)

    high = Column(Float)

    low = Column(Float)

    close = Column(Float)

    volume = Column(BigInteger)

    payload_id = Column(
        BigInteger,
        ForeignKey("raw_market_payloads.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


    instrument = relationship(
        "Instrument",
        back_populates="raw_data"
    )

    payload = relationship(
        "RawMarketPayload",
        back_populates="market_data"
    )


class DownloadBatch(Base):

    __tablename__ = "download_batches"

    id = Column(
        Integer,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id")
    )

    from_date = Column(
        DateTime
    )

    to_date = Column(
        DateTime
    )

    interval = Column(
        String(10)
    )

    status = Column(
        String(20)
    )

    records_downloaded = Column(
        Integer
    )

    error_message = Column(
        String
    )


class ProcessingRun(Base):

    __tablename__ = "processing_runs"

    id = Column(
        Integer,
        primary_key=True
    )

    process_name = Column(
        String(100)
    )

    input_table = Column(
        String(100)
    )

    output_table = Column(
        String(100)
    )

    status = Column(
        String(20)
    )

    started_at = Column(
        DateTime,
        server_default=func.now()
    )

    completed_at = Column(
        DateTime
    )

    code_version = Column(
        String(50)
    )

    error_message = Column(
        Text
    )



class ProcessedMarketData(Base):

    __tablename__ = "processed_market_data"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_processed_market_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(
        Float
    )

    high = Column(
        Float
    )

    low = Column(
        Float
    )

    close = Column(
        Float
    )

    volume = Column(
        BigInteger
    )

    lastclose = Column(
        Float
    )

    source_raw_id = Column(
        BigInteger,
        ForeignKey("raw_market_data.id")
    )

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime
    )


class BaseCandle:

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_candle_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(
        Float
    )

    high = Column(
        Float
    )

    low = Column(
        Float
    )

    close = Column(
        Float
    )

    volume = Column(
        BigInteger
    )

    lastclose = Column(
        Float
    )

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Candle2M(Base):

    __tablename__ = "candles_2m"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_candles_2m_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    lastclose = Column(Float)

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Candle3M(Base):

    __tablename__ = "candles_3m"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_candles_3m_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    lastclose = Column(Float)

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )



class Candle5M(Base):

    __tablename__ = "candles_5m"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_candles_5m_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    lastclose = Column(Float)

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )



class Candle15M(Base):

    __tablename__ = "candles_15m"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            name="uq_candles_15m_instrument_timestamp"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )

    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    lastclose = Column(Float)

    processing_run_id = Column(
        Integer,
        ForeignKey("processing_runs.id")
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class CandleAnalytics(Base):

    __tablename__ = "candle_analytics"

    __table_args__ = (

        UniqueConstraint(
            "instrument_id",
            "timestamp",
            "timeframe",
            name="uq_candle_analytics_key"
        ),

    )

    id = Column(
        BigInteger,
        primary_key=True
    )


    instrument_id = Column(
        Integer,
        ForeignKey("instruments.id"),
        nullable=False
    )


    timestamp = Column(
        DateTime,
        nullable=False
    )


    timeframe = Column(
        String(10),
        nullable=False
    )


    return_pct = Column(
        Float
    )

    vwap = Column(
        Float
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )