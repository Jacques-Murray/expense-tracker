"""UI tests for the Expense Tracker web interface."""
import os
import time
import unittest
from datetime import datetime
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from expense_tracker.web.app import app
from expense_tracker.web.config import CURRENCIES, DATE_FORMATS
from expense_tracker.models.expense_manager import ExpenseManager


class TestWebInterface(unittest.TestCase):
    """Test cases for the Expense Tracker web interface."""

    @classmethod
    def setUpClass(cls):
        """Set up test class - runs once before all tests."""
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize WebDriver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)  # seconds
        
        # Start Flask server
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        cls.app = app.test_client()
        
        # Clear any existing test data
        manager = ExpenseManager()
        manager.clear_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.driver.quit()

    def setUp(self):
        """Set up each test."""
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('http://localhost:5000')

    def test_homepage_loads(self):
        """Test that the homepage loads correctly."""
        # Check title
        self.assertEqual("Dashboard - Expense Tracker", self.driver.title)
        
        # Check main components
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "navbar").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "expenseChart").is_displayed())
        
        # Check quick stats cards
        stats_cards = self.driver.find_elements(By.CLASS_NAME, "card")
        self.assertGreaterEqual(len(stats_cards), 3)  # At least 3 stats cards

    def test_add_expense(self):
        """Test adding a new expense."""
        # Click add expense button
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-target='#addExpenseModal']"))
        )
        add_button.click()
        
        # Fill in expense form
        modal = self.wait.until(
            EC.visibility_of_element_located((By.ID, "addExpenseModal"))
        )
        amount_input = modal.find_element(By.ID, "amount")
        amount_input.send_keys("50.00")
        
        category_select = Select(modal.find_element(By.ID, "category"))
        category_select.select_by_value("Food")
        
        description_input = modal.find_element(By.ID, "description")
        description_input.send_keys("Test expense")
        
        # Submit form
        submit_button = modal.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verify expense was added
        time.sleep(1)  # Wait for page to update
        expenses_table = self.driver.find_element(By.CSS_SELECTOR, "table tbody")
        expense_rows = expenses_table.find_elements(By.TAG_NAME, "tr")
        self.assertGreaterEqual(len(expense_rows), 1)
        
        latest_expense = expense_rows[0]
        self.assertIn("Food", latest_expense.text)
        self.assertIn("Test expense", latest_expense.text)
        self.assertIn("50.00", latest_expense.text)

    def test_change_settings(self):
        """Test changing currency and date format settings."""
        # Navigate to settings page
        settings_link = self.driver.find_element(By.LINK_TEXT, "Settings")
        settings_link.click()
        
        # Change currency to EUR
        currency_select = Select(self.driver.find_element(By.ID, "currency"))
        currency_select.select_by_value("EUR")
        
        # Change date format to EU
        date_format_select = Select(self.driver.find_element(By.ID, "date_format"))
        date_format_select.select_by_value("EU")
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verify settings were saved
        self.driver.get('http://localhost:5000/settings')
        currency_select = Select(self.driver.find_element(By.ID, "currency"))
        date_format_select = Select(self.driver.find_element(By.ID, "date_format"))
        
        self.assertEqual("EUR", currency_select.first_selected_option.get_attribute("value"))
        self.assertEqual("EU", date_format_select.first_selected_option.get_attribute("value"))

    def test_delete_expense(self):
        """Test deleting an expense."""
        # First add an expense
        self.test_add_expense()
        
        # Find and click delete button
        delete_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-danger"))
        )
        delete_button.click()
        
        # Wait for delete to complete and verify
        time.sleep(1)  # Wait for deletion
        expenses_table = self.driver.find_element(By.CSS_SELECTOR, "table tbody")
        expense_rows = expenses_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(expense_rows), 0)

    def test_expense_filters(self):
        """Test expense list filters."""
        # Add two different expenses
        self.test_add_expense()  # Adds a Food expense
        
        # Add another expense in different category
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-target='#addExpenseModal']"))
        )
        add_button.click()
        
        modal = self.wait.until(
            EC.visibility_of_element_located((By.ID, "addExpenseModal"))
        )
        amount_input = modal.find_element(By.ID, "amount")
        amount_input.send_keys("75.00")
        
        category_select = Select(modal.find_element(By.ID, "category"))
        category_select.select_by_value("Transport")
        
        description_input = modal.find_element(By.ID, "description")
        description_input.send_keys("Transport expense")
        
        submit_button = modal.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Navigate to expenses page
        self.driver.get('http://localhost:5000/expenses')
        
        # Test category filter
        category_filter = Select(self.driver.find_element(By.ID, "filterCategory"))
        category_filter.select_by_value("Food")
        
        # Submit filter form
        filter_form = self.driver.find_element(By.ID, "filterForm")
        filter_form.submit()
        
        # Verify filtered results
        time.sleep(1)  # Wait for filter to apply
        expenses_table = self.driver.find_element(By.CSS_SELECTOR, "table tbody")
        expense_rows = expenses_table.find_elements(By.TAG_NAME, "tr")
        self.assertEqual(len(expense_rows), 1)
        self.assertIn("Food", expense_rows[0].text)

    def test_stats_page(self):
        """Test statistics page functionality."""
        # Add some expenses first
        self.test_add_expense()  # Adds a Food expense
        
        # Navigate to stats page
        stats_link = self.driver.find_element(By.LINK_TEXT, "Statistics")
        stats_link.click()
        
        # Check stats components
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "card").is_displayed())
        
        # Verify category stats
        category_stats = self.driver.find_elements(By.CLASS_NAME, "progress-bar")
        self.assertGreaterEqual(len(category_stats), 1)


if __name__ == '__main__':
    unittest.main()
