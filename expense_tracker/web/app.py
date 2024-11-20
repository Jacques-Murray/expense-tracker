"""Flask application for the Expense Tracker web interface."""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict

from flask import Flask, flash, jsonify, render_template, request

from expense_tracker.models.expense_manager import ExpenseManager

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this in production

# Initialize expense manager
manager = ExpenseManager()

# Category colors for badges
CATEGORY_COLORS = {
    "Food": "success",
    "Transport": "info",
    "Entertainment": "primary",
    "Bills": "danger",
    "Shopping": "warning",
    "Others": "secondary",
}


@app.route("/")
def index():
    """Render the dashboard page."""
    current_date = datetime.now()
    start_date = datetime(current_date.year, current_date.month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get expenses for the current month
    expenses = manager.get_expenses()
    monthly_expenses = [e for e in expenses if start_date <= e.date <= end_date]

    # Calculate statistics
    monthly_total = sum(e.amount for e in monthly_expenses)
    daily_average = monthly_total / end_date.day if monthly_expenses else Decimal("0")
    budget_percentage = min(int((monthly_total / Decimal("1000")) * 100), 100)

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
        recent_expenses=sorted(expenses, key=lambda x: x.date, reverse=True)[:5],
        monthly_total=monthly_total,
        daily_average=daily_average,
        budget_percentage=budget_percentage,
        dates=dates,
        daily_expenses=daily_expenses,
        categories=list(CATEGORY_COLORS.keys()),
        category_colors=CATEGORY_COLORS,
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
                "amount": amount,
                "percentage": percentage,
                "color": CATEGORY_COLORS.get(category, "secondary"),
            }
        )

    return render_template(
        "stats.html",
        category_stats=category_stats,
        total=total,
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


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id: int):
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
                "amount": float(e.amount),
            }
        )

    return jsonify(
        {
            "dates": dates,
            "daily_expenses": daily_expenses,
            "monthly_total": float(monthly_total),
            "daily_average": float(daily_average),
            "budget_percentage": budget_percentage,
            "recent_expenses": recent_expenses,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
