from typing import Optional, Dict

from pydantic import BaseModel

from src.dto.market_data import MarketData


# TODO: TimePointGoldGenA0
class TimePoint(BaseModel):
    current_etf: MarketData = None
    future_etf: MarketData = None
    top1_company: MarketData = None
    top2_company: MarketData = None
    top3_company: MarketData = None
    crude_oil: MarketData = None
    esg_regulations: MarketData = None

    sp500: MarketData = None
    stoxx600: MarketData = None
    bitcoin: MarketData = None

    eur_to_dollar: MarketData = None
    aud_to_dollar: MarketData = None
    zar_to_dollar: MarketData = None
    cad_to_dollar: MarketData = None

    euribor_ecb: MarketData = None
    libor: MarketData = None
    treasury_bond7_us: MarketData = None

    us_vix: MarketData = None
    eu_vix: MarketData = None
    us_cpi: MarketData = None
    eu_cpi: MarketData = None
    us_gdp: MarketData = None
    eu_gdp: MarketData = None
    us_dxy: MarketData = None
    eu_exy: MarketData = None
    us_housing_market_reit_etf: MarketData = None
    eu_housing_market_reit_etf: MarketData = None

    # remaining_days: Optional[RemainingDays]  # Uncomment if this is defined

    # Dictionary mapping field names to tickers
    field_tickers: Dict[str, str] = {
        "current_etf": "SGLD.L",
        "future_etf": "GC=F",
        "top1_company": "NEM",
        "top2_company": "AU",
        "top3_company": "RGLD",
        "crude_oil": "DBO",
        "esg_regulations": "SUSA",
        "sp500": "%5EGSPC",
        "stoxx600": "%5ESTOXX",
        "bitcoin": "BTC-USD",
        "eur_to_dollar": "EURUSD=X",
        "aud_to_dollar": "AUDUSD=X",
        "zar_to_dollar": "ZARUSD=X",
        "cad_to_dollar": "CADUSD=X",
        "euribor_ecb": "IBGE.L",
        "libor": "BKLN",
        "treasury_bond7_us": "IEF",
        "us_vix": "%5EVIX",
        "eu_vix": "FEZ",
        "us_cpi": "TIP",
        "eu_cpi": "IBCI.DE",
        "us_gdp": "SPY",
        "eu_gdp": "EZU",
        "us_dxy": "DX-Y.NYB",
        "eu_exy": "FXE",
        "us_housing_market_reit_etf": "IYR",
        "eu_housing_market_reit_etf": "IPRP.L"
    }

    def get_ticker_for_field(self, field_name: str) -> Optional[str]:
        """Returns the ticker symbol associated with a specific field name."""
        return self.field_tickers.get(field_name)

    # @validator("*", pre=True, always=True)
    # def check_validity(cls, value, field):
    #     """Ensures all MarketData fields are populated."""
    #     if value is None:
    #         raise ValueError(f"{field.name} cannot be None.")
    #     return value

    def is_valid(self) -> bool:
        """Check if all fields are non-null and valid."""
        return all(getattr(self, field) is not None for field in self.__annotations__)

    def is_workday(self) -> bool:
        """Checks if the day of the week for any provided MarketData is a workday (less than 6)."""
        for field_name, field_type in self.__annotations__.items():
            field_value = getattr(self, field_name)
            if field_value and field_value.day_of_week is not None and field_value.day_of_week < 6:
                return True
        return False

    class Config:
        arbitrary_types_allowed = True
