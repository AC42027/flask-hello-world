from flask import Flask, request, render_template_string

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


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
        <html>
        <head>
            <title>Monthly Budget</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 2rem auto;
                    padding: 0 1rem;
                    background: #fafafa;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                form {
                    margin-bottom: 1.5rem;
                    background: #fff;
                    padding: 1rem;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }
                label, input {
                    display: block;
                    width: 100%;
                    margin-top: 0.5rem;
                }
                button {
                    margin-top: 0.5rem;
                    padding: 0.5rem 1rem;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    padding: 0.25rem 0;
                    border-bottom: 1px solid #eee;
                }
                .summary {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Monthly Budget</h1>
            <form method="post">
                <label>Set monthly budget:
                    <input name="limit" type="number" step="0.01" value="{{ limit }}">
                </label>
                <button type="submit">Save</button>
            </form>
            <form method="post">
                <label>Expense name:
                    <input name="name" placeholder="Expense name">
                </label>
                <label>Amount:
                    <input name="amount" type="number" step="0.01" placeholder="Amount">
                </label>
                <button type="submit">Add</button>
            </form>
            <h2>Summary</h2>
            <ul>
                {% for e in expenses %}
                <li>{{ e.name }}: {{ e.amount }}</li>
                {% endfor %}
            </ul>
            <p class="summary">Total spent: {{ total_spent }}</p>
            <p class="summary">Remaining: {{ remaining }}</p>
        </body>
        </html>
        """,
        limit=budget_data["limit"],
        expenses=budget_data["expenses"],
        total_spent=total_spent,
        remaining=remaining,
    )
