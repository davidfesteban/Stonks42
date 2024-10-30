from dataclasses import dataclass
from typing import Optional, Dict

from src.dto.market_data import MarketData


# TODO: TimePointGoldGenA0
@dataclass
class TimePoint:
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
    @staticmethod
    def get_field_tickers() -> Dict[str, str]:
        return {
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

    class Config:
        arbitrary_types_allowed = True
