"""Flask application for the Expense Tracker web interface."""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from expense_tracker.models.expense_manager import ExpenseManager
from expense_tracker.web.config import (
    CURRENCIES,
    DATE_FORMATS,
    DEFAULT_BUDGET,
    DEFAULT_CURRENCY,
    DEFAULT_DATE_FORMAT,
)

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this in production

# Initialize expense manager
manager = ExpenseManager()


@app.template_filter("format_date")
def format_date_filter(date):
    """Format date according to current regional settings."""
    date_format = DATE_FORMATS[session.get("date_format", DEFAULT_DATE_FORMAT)]
    return date.strftime(date_format)


# Category colors for badges
CATEGORY_COLORS = {
    "Food": "success",
    "Transport": "info",
    "Entertainment": "primary",
    "Bills": "danger",
    "Shopping": "warning",
    "Others": "secondary",
}


def get_current_settings():
    """Get current user settings with defaults."""
    return {
        "currency": session.get("currency", DEFAULT_CURRENCY),
        "date_format": session.get("date_format", DEFAULT_DATE_FORMAT),
        "monthly_budget": session.get("monthly_budget", DEFAULT_BUDGET),
    }


def format_amount(amount: Decimal) -> str:
    """Format amount according to current currency settings."""
    currency = CURRENCIES[session.get("currency", DEFAULT_CURRENCY)]
    formatted = f"{float(amount):,.2f}"

    # Handle separators
    if currency.decimal_separator != ".":
        formatted = formatted.replace(".", currency.decimal_separator)
    if currency.thousands_separator != ",":
        formatted = formatted.replace(",", currency.thousands_separator)

    # Format with currency symbol
    if currency.position == "prefix":
        # No space for USD, GBP
        if currency.code in ["USD", "GBP"]:
            return f"{currency.symbol}{formatted}"
        # Single space for others
        return f"{currency.symbol} {formatted}"
    # Space before symbol for suffix position
    return f"{formatted} {currency.symbol}"


def format_date(date: datetime) -> str:
    """Format date according to current regional settings."""
    date_format = DATE_FORMATS[session.get("date_format", DEFAULT_DATE_FORMAT)]
    return date.strftime(date_format)


@app.route("/")
def index():
    """Render the dashboard page."""
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get current settings
    settings = get_current_settings()
    monthly_budget = Decimal(str(settings["monthly_budget"]))

    # Get expenses for the current month
    expenses = manager.get_expenses()
    monthly_expenses = [e for e in expenses if start_date <= e.date <= end_date]

    # Calculate statistics
    monthly_total = sum(e.amount for e in monthly_expenses)
    daily_average = monthly_total / end_date.day if monthly_expenses else Decimal("0")
    budget_percentage = (
        min(int((monthly_total / monthly_budget) * 100), 100) if monthly_budget else 0
    )

    # Format recent expenses
    recent_expenses = []
    for expense in sorted(expenses, key=lambda x: x.date, reverse=True)[:5]:
        recent_expenses.append(
            {
                "date": expense.date,
                "description": expense.description,
                "category": expense.category,
                "category_color": CATEGORY_COLORS.get(expense.category, "secondary"),
                "amount": format_amount(expense.amount),
            }
        )

    # Prepare data for the chart
    dates = []
    daily_expenses = []
    current = start_date
    while current <= end_date:
        dates.append(current.strftime("%Y-%m-%d"))
        day_expenses = sum(
            e.amount for e in monthly_expenses if e.date.date() == current.date()
        )
        daily_expenses.append(float(day_expenses))
        current += timedelta(days=1)

    return render_template(
        "index.html",
        current_month=start_date.strftime("%B %Y"),
        recent_expenses=recent_expenses,
        monthly_total=format_amount(monthly_total),
        daily_average=format_amount(daily_average),
        budget_percentage=budget_percentage,
        monthly_budget=format_amount(monthly_budget),
        dates=dates,
        daily_expenses=daily_expenses,
        CURRENCIES=CURRENCIES,
    )


@app.route("/expenses")
def expenses():
    """Render the expenses page."""
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    expenses = manager.get_expenses()

    if category:
        expenses = [e for e in expenses if e.category == category]
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        expenses = [e for e in expenses if e.date >= start]
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        expenses = [e for e in expenses if e.date <= end]

    return render_template(
        "expenses.html",
        expenses=sorted(expenses, key=lambda x: x.date, reverse=True),
        categories=list(CATEGORY_COLORS.keys()),
        category_colors=CATEGORY_COLORS,
        selected_category=category,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/stats")
def stats():
    """Render the statistics page."""
    expenses = manager.get_expenses()

    # Calculate category totals
    category_totals: Dict[str, Decimal] = {}
    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = Decimal("0")
        category_totals[expense.category] += expense.amount

    # Calculate percentages
    total = sum(category_totals.values())
    category_stats = []
    for category, amount in sorted(category_totals.items()):
        percentage = (amount / total * 100) if total else Decimal("0")
        category_stats.append(
            {
                "category": category,
                "amount": format_amount(amount),
                "percentage": percentage,
                "color": CATEGORY_COLORS.get(category, "secondary"),
            }
        )

    return render_template(
        "stats.html",
        category_stats=category_stats,
        total=format_amount(total),
    )


@app.route("/add_expense", methods=["POST"])
def add_expense():
    """Add a new expense."""
    try:
        amount = Decimal(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]

        if amount <= 0:
            raise ValueError("Amount must be positive")

        expense = manager.add_expense(
            amount=amount,
            category=category,
            description=description,
            date=datetime.now(),
        )

        flash("Expense added successfully!", "success")
        return jsonify({"success": True, "expense": expense.to_dict()})

    except (ValueError, KeyError) as e:
        flash(f"Error: {str(e)}", "danger")
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/expenses/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id: str):
    """Delete an expense."""
    try:
        manager.delete_expense(expense_id)
        return jsonify({"success": True})
    except KeyError:
        return (
            jsonify(
                {"success": False, "message": f"No expense found with ID {expense_id}"}
            ),
            404,
        )


@app.route("/api/dashboard")
def dashboard_data():
    """Get dashboard data for a specific date."""
    try:
        date = datetime.fromisoformat(request.args["date"].replace("Z", "+00:00"))
    except (KeyError, ValueError):
        date = datetime.now()

    start_date = datetime(date.year, date.month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    expenses = manager.get_expenses()
    monthly_expenses = [e for e in expenses if start_date <= e.date <= end_date]

    monthly_total = sum(e.amount for e in monthly_expenses)
    daily_average = monthly_total / end_date.day if monthly_expenses else Decimal("0")
    budget_percentage = min(int((monthly_total / Decimal("1000")) * 100), 100)

    dates = []
    daily_expenses = []
    current = start_date
    while current <= end_date:
        dates.append(current.strftime("%Y-%m-%d"))
        day_expenses = sum(
            e.amount for e in monthly_expenses if e.date.date() == current.date()
        )
        daily_expenses.append(float(day_expenses))
        current += timedelta(days=1)

    recent_expenses = []
    for e in sorted(expenses, key=lambda x: x.date, reverse=True)[:5]:
        recent_expenses.append(
            {
                "date": e.date.isoformat(),
                "category": e.category,
                "category_color": CATEGORY_COLORS.get(e.category, "secondary"),
                "description": e.description,
                "amount": format_amount(e.amount),
            }
        )

    return jsonify(
        {
            "dates": dates,
            "daily_expenses": daily_expenses,
            "monthly_total": format_amount(monthly_total),
            "daily_average": format_amount(daily_average),
            "budget_percentage": budget_percentage,
            "recent_expenses": recent_expenses,
        }
    )


@app.route("/settings", methods=["GET"])
def settings():
    """Render the settings page."""
    current = get_current_settings()

    # Generate date format examples with descriptions
    date_examples = {
        format_name: {
            "example": datetime.now().strftime(format_str),
            "description": {
                "US": "American (MM/DD/YYYY)",
                "EU": "European (DD/MM/YYYY)",
                "ISO": "International (YYYY-MM-DD)",
                "UK": "British (DD/MM/YYYY)",
                "JP": "Japanese (YYYY/MM/DD)",
                "ZA": "South African (YYYY/MM/DD)",
            }[format_name],
        }
        for format_name, format_str in DATE_FORMATS.items()
    }

    return render_template(
        "settings.html",
        currencies=CURRENCIES,
        date_formats=date_examples,
        current_currency=current["currency"],
        current_date_format=current["date_format"],
        monthly_budget=current["monthly_budget"],
        currency_symbol=CURRENCIES[current["currency"]].symbol,
    )


@app.route("/settings", methods=["POST"])
def save_settings():
    """Save user settings."""
    currency = request.form.get("currency")
    date_format = request.form.get("date_format")
    monthly_budget = request.form.get("monthly_budget")

    if currency in CURRENCIES:
        session["currency"] = currency
    if date_format in DATE_FORMATS:
        session["date_format"] = date_format
    if monthly_budget:
        try:
            session["monthly_budget"] = float(monthly_budget)
        except ValueError:
            flash("Invalid budget amount", "error")

    flash("Settings saved successfully!", "success")
    return redirect(url_for("settings"))


if __name__ == "__main__":
    app.run(debug=True)
