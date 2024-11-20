"""Configuration settings for the expense tracker web interface."""
from dataclasses import dataclass
from typing import Dict, List

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
    'USD': CurrencyConfig('USD', '$', 'prefix', '.', ','),
    'EUR': CurrencyConfig('EUR', '€', 'suffix', ',', '.'),
    'GBP': CurrencyConfig('GBP', '£', 'prefix', '.', ','),
    'JPY': CurrencyConfig('JPY', '¥', 'prefix', '.', ','),
    'INR': CurrencyConfig('INR', '₹', 'prefix', '.', ','),
    'CNY': CurrencyConfig('CNY', '¥', 'prefix', '.', ','),
    'ZAR': CurrencyConfig('ZAR', 'R', 'prefix', '.', ','),
    'AUD': CurrencyConfig('AUD', 'A$', 'prefix', '.', ','),
    'CAD': CurrencyConfig('CAD', 'C$', 'prefix', '.', ','),
    'NZD': CurrencyConfig('NZD', 'NZ$', 'prefix', '.', ','),
}

# Date format configurations by region
DATE_FORMATS: Dict[str, str] = {
    'US': '%m/%d/%Y',
    'EU': '%d/%m/%Y',
    'ISO': '%Y-%m-%d',
    'UK': '%d/%m/%Y',
    'JP': '%Y年%m月%d日',
}

# Default settings
DEFAULT_CURRENCY = 'USD'
DEFAULT_DATE_FORMAT = 'US'
DEFAULT_BUDGET = 1000  # Default monthly budget
