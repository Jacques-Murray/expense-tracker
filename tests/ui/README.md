# UI Tests for Expense Tracker

This directory contains UI tests for the Expense Tracker web interface using Selenium WebDriver.

## Test Coverage

The test suite covers the following functionality:

1. Homepage Loading
   - Verifies that the dashboard loads correctly
   - Checks for presence of key UI components
   - Validates quick stats cards

2. Expense Management
   - Adding new expenses
   - Deleting existing expenses
   - Filtering expenses by category
   - Validating expense data display

3. Settings Management
   - Changing currency settings
   - Updating date format preferences
   - Verifying settings persistence

4. Statistics Page
   - Checking statistics display
   - Validating category breakdowns
   - Verifying data visualization components

## Running the Tests

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask application in a separate terminal:
```bash
python -m flask --app wsgi run
```
or
```bash
python wsgi.py
```

3. Run the tests:
```bash
pytest tests/ui/test_web_interface.py -v
```

## Test Configuration

- Tests run in headless Chrome by default
- Each test uses a fresh database state
- Automatic cleanup of test data between runs
- 10-second implicit wait for elements
- CSRF protection disabled for testing

## Adding New Tests

When adding new UI tests:

1. Add the test method to `TestWebInterface` class
2. Follow the existing pattern of:
   - Arrange (set up test data)
   - Act (perform UI actions)
   - Assert (verify results)
3. Use WebDriverWait for dynamic elements
4. Clean up any test data in tearDown if needed

## Common Selectors

- Add Expense Button: `[data-bs-target='#addExpenseModal']`
- Expense Table: `table tbody`
- Category Filter: `#filterCategory`
- Settings Dropdowns: `#currency`, `#date_format`
- Delete Button: `button.btn-danger`

## Known Limitations

1. Tests require Chrome/Chromium browser
2. Flask server must be running
3. Network connectivity required for WebDriver manager
4. Some tests have fixed waits (sleep)
