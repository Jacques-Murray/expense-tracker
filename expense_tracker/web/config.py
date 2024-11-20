"""Configuration settings for the expense tracker web interface."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class CurrencyConfig:
    """Currency configuration settings."""

    code: str
    symbol: str
    position: str  # 'prefix' or 'suffix'
    decimal_separator: str
    thousands_separator: str


# Common currency configurations
CURRENCIES: Dict[str, CurrencyConfig] = {
    "USD": CurrencyConfig("USD", "$", "prefix", ".", ","),
    "EUR": CurrencyConfig("EUR", "€", "suffix", ",", "."),
    "GBP": CurrencyConfig("GBP", "£", "prefix", ".", ","),
    "JPY": CurrencyConfig("JPY", "¥", "prefix", ".", ","),
    "INR": CurrencyConfig("INR", "₹", "prefix", ".", ","),
    "CNY": CurrencyConfig("CNY", "¥", "prefix", ".", ","),
    "ZAR": CurrencyConfig("ZAR", "R", "prefix", ".", ","),  # South African Rand
    "AUD": CurrencyConfig("AUD", "$", "prefix", ".", ","),  # Changed from A$
    "CAD": CurrencyConfig("CAD", "$", "prefix", ".", ","),  # Changed from C$
    "NZD": CurrencyConfig("NZD", "$", "prefix", ".", ","),  # Changed from NZ$
}

# Date format configurations by region
DATE_FORMATS: Dict[str, str] = {
    "US": "%m/%d/%Y",  # MM/DD/YYYY
    "EU": "%d/%m/%Y",  # DD/MM/YYYY
    "ISO": "%Y-%m-%d",  # YYYY-MM-DD
    "UK": "%d/%m/%Y",  # DD/MM/YYYY
    "JP": "%Y/%m/%d",  # YYYY/MM/DD
    "ZA": "%Y/%m/%d",  # YYYY/MM/DD
}

# Default settings
DEFAULT_CURRENCY = "USD"
DEFAULT_DATE_FORMAT = "US"
DEFAULT_BUDGET = 1000  # Default monthly budget
