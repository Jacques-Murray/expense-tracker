"""Setup configuration for the Expense Tracker package."""
from setuptools import setup, find_packages

setup(
    name="expense-tracker",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        "flask>=3.0.2",
        "flask-wtf>=1.2.1",
        "pandas>=2.0.3",
        "matplotlib>=3.7.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pre-commit>=3.5.0",
            "black>=24.3.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "flake8-docstrings>=1.7.0",
            "flake8-bugbear>=23.9.16",
            "flake8-comprehensions>=3.14.0",
            "flake8-simplify>=0.21.0",
            "mypy>=1.7.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "selenium>=4.11.2",
            "webdriver-manager>=4.0.0",
        ],
    },
)
