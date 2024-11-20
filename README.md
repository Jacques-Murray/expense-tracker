# Expense Tracker

A Python-based GUI application for tracking daily expenses with visualization capabilities.

## Features

- Add, update, and delete expenses
- Categorize expenses (Food, Transport, Entertainment, Bills, Shopping, Other)
- View expenses in a organized table format
- Visualize expenses with charts:
  - Pie chart showing category-wise distribution
  - Bar chart showing daily expense trends
- Export expenses to CSV file

## Requirements

- Python 3.8 or higher (tested up to Python 3.12)
- Required packages:
  - pandas
  - matplotlib

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python expense_tracker.py
```

## How to Use

1. **Adding Expenses**:
   - Enter the amount
   - Select a category
   - Add a description (optional)
   - Click "Add Expense"

2. **Managing Expenses**:
   - View all expenses in the table
   - Select and delete unwanted expenses
   - Export expenses to CSV for external analysis

3. **Visualizing Data**:
   - Click "Show Charts" to view:
     - Category-wise distribution
     - Daily expense trends

## Data Storage

Expenses are stored locally in a JSON file (`expenses.json`) for persistence between sessions.
