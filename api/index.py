from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the Budget App!"


@app.route("/about")
def about():
    return "About"


budget_data = {"limit": 0.0, "expenses": []}


@app.route("/budget", methods=["GET", "POST"])
def budget():
    """Simple in-memory monthly budget tracker."""
    if request.method == "POST":
        if "limit" in request.form:
            try:
                budget_data["limit"] = float(request.form["limit"])
            except ValueError:
                pass
        elif "name" in request.form and "amount" in request.form:
            try:
                amount = float(request.form["amount"])
                budget_data["expenses"].append(
                    {"name": request.form["name"], "amount": amount}
                )
            except ValueError:
                pass
    total_spent = sum(e["amount"] for e in budget_data["expenses"])
    remaining = budget_data["limit"] - total_spent
    return render_template_string(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Monthly Budget</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
                form { margin-bottom: 1em; }
                input, button { margin-right: 0.5em; }
                ul { list-style: none; padding: 0; }
            </style>
        </head>
        <body>
            <h1>Monthly Budget</h1>
            <form method="post">
                <label>Set monthly budget: <input name="limit" type="number" step="0.01" value="{{ limit }}"></label>
                <button type="submit">Save</button>
            </form>
            <h2>Add Expense</h2>
            <form method="post">
                <input name="name" placeholder="Expense name">
                <input name="amount" type="number" step="0.01" placeholder="Amount">
                <button type="submit">Add</button>
            </form>
            <h2>Summary</h2>
            <ul>
                {% for e in expenses %}
                <li>{{ e.name }}: {{ e.amount }}</li>
                {% endfor %}
            </ul>
            <p>Total spent: {{ total_spent }}</p>
            <p>Remaining: {{ remaining }}</p>
        </body>
        </html>
        """,
        limit=budget_data["limit"],
        expenses=budget_data["expenses"],
        total_spent=total_spent,
        remaining=remaining,
    )
