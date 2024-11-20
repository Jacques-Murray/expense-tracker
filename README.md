# Expense Tracker

A modern web-based expense tracking application built with Flask and Bootstrap. Track your expenses, visualize spending patterns, and manage your budget with ease.

## Features

- **Dashboard Overview**
  - Monthly expense summary
  - Daily average spending
  - Budget progress visualization
  - Daily expense chart
  - Quick add expense form

- **Expense Management**
  - Add, view, and delete expenses
  - Categorize expenses
  - Filter expenses by category and date range
  - Sort expenses by date

- **Statistics and Visualization**
  - Category-wise expense breakdown
  - Visual representation with charts
  - Percentage analysis of spending

- **Customization**
  - Multiple currency support (USD, EUR, GBP, ZAR, etc.)
  - Configurable date formats
  - Adjustable monthly budget

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Configuration

1. Create a `.env` file in the root directory:
```env
FLASK_APP=expense_tracker.web.app
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

2. Initialize the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`.

## Usage

1. **Dashboard**
   - View your monthly spending overview
   - Track budget progress
   - Add quick expenses
   - View recent transactions

2. **Expenses**
   - Add detailed expenses with categories
   - Filter and sort your expense history
   - Delete unwanted entries

3. **Statistics**
   - Analyze spending patterns
   - View category-wise breakdowns
   - Track expense distribution

4. **Settings**
   - Choose your preferred currency
   - Set date format
   - Configure monthly budget

## Development

### Project Structure
```
expense_tracker/
├── expense_tracker/
│   ├── models/
│   │   ├── expense.py
│   │   └── expense_manager.py
│   └── web/
│       ├── app.py
│       ├── config.py
│       └── templates/
├── tests/
│   ├── unit/
│   └── ui/
├── .env
├── .flaskenv
├── pyproject.toml
└── setup.py
```

### Testing

Run the test suite:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
