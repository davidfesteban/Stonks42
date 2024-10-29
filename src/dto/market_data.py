from typing import Optional

from pydantic import BaseModel, Field

class MarketData(BaseModel):
    date: Optional[int]  # Unix timestamp for easier storage
    day_of_week: Optional[int] = Field(None, description="Day of the week as an integer (0 for Sunday, 6 for Saturday)")

    etf_open: Optional[float] = Field(None, description="Opening price of the ETF")
    etf_close: Optional[float] = Field(None, description="Closing price of the ETF")
    etf_low: Optional[float] = Field(None, description="Lowest price of the ETF")
    etf_high: Optional[float] = Field(None, description="Highest price of the ETF")
    etf_volume: Optional[float] = Field(None, description="Volume of the ETF")

    average_5_days_volume: Optional[float] = Field(None, description="5-day average volume")
    average_10_days_volume: Optional[float] = Field(None, description="10-day average volume")
    average_20_days_volume: Optional[float] = Field(None, description="20-day average volume")
    average_30_days_volume: Optional[float] = Field(None, description="30-day average volume")
    average_50_days_volume: Optional[float] = Field(None, description="50-day average volume")
    average_100_days_volume: Optional[float] = Field(None, description="100-day average volume")
    average_200_days_volume: Optional[float] = Field(None, description="200-day average volume")

    average_5_days_close: Optional[float] = Field(None, description="5-day average closing price")
    average_10_days_close: Optional[float] = Field(None, description="10-day average closing price")
    average_20_days_close: Optional[float] = Field(None, description="20-day average closing price")
    average_30_days_close: Optional[float] = Field(None, description="30-day average closing price")
    average_50_days_close: Optional[float] = Field(None, description="50-day average closing price")
    average_100_days_close: Optional[float] = Field(None, description="100-day average closing price")
    average_200_days_close: Optional[float] = Field(None, description="200-day average closing price")

    etf_week_52_low: Optional[float] = Field(None, description="52-week low price of the ETF")
    etf_week_52_high: Optional[float] = Field(None, description="52-week high price of the ETF")

    volatility_10_days: Optional[float] = Field(None, description="10-day volatility of the ETF")
    volatility_20_days: Optional[float] = Field(None, description="20-day volatility of the ETF")
    volatility_30_days: Optional[float] = Field(None, description="30-day volatility of the ETF")