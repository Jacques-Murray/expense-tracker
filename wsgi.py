"""WSGI entry point for the Expense Tracker application."""
from expense_tracker.web.app import app

if __name__ == "__main__":
    app.run(debug=True)
