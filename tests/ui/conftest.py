"""Test configuration and fixtures for UI tests."""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from expense_tracker.web.app import app
from expense_tracker.models.expense_manager import ExpenseManager


@pytest.fixture(scope="session")
def flask_app():
    """Create a Flask application for testing."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture(scope="session")
def chrome_driver():
    """Create a Chrome WebDriver instance."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture(autouse=True)
def clean_data():
    """Clean test data before each test."""
    manager = ExpenseManager()
    manager.clear_all()
    yield
