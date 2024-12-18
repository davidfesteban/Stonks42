import math
from typing import Optional

from pydantic import BaseModel, Field


class MarketData(BaseModel):
    date: Optional[int]  # Formatted as YYYYMMDD
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

    def fill_na_with_zero(self):
        for field, value in self.__dict__.items():
            if value is None or (isinstance(value, float) and math.isnan(value)):
                setattr(self, field, 0)
        return self

    def fill_none_with_na(self):
        for field, value in self.__dict__.items():
            if value is None or (isinstance(value, float) and math.isnan(value)):
                setattr(self, field, math.nan)
        return self

    def is_valid_correcting_volume(self) -> bool:
        # Check that all fields are not None and greater than 0
        if (self.etf_open is None or self.etf_open <= 0 or
                self.etf_close is None or self.etf_close <= 0 or
                self.etf_low is None or self.etf_low <= 0 or
                self.etf_high is None or self.etf_high <= 0):
            return False

        if self.etf_volume is None or self.etf_volume == 0 and self.etf_open != self.etf_close:
            self.etf_volume = math.nan

        return True
