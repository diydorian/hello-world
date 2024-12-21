from flask import Flask, request, render_template_string, jsonify
from dataclasses import dataclass, asdict
from typing import List, Dict

app = Flask(__name__)

@dataclass
class Expense:
    category: str
    amount: float

@dataclass
class Budget:
    income: float
    expenses: List[Expense]

    def total_expenses(self) -> float:
        return sum(expense.amount for expense in self.expenses)

    def remaining_income(self) -> float:
        return self.income - self.total_expenses()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(template)

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Budget Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .expense-row { margin-bottom: 10px; }
        button { margin-top: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        #remaining { font-weight: bold; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Budget Calculator</h1>
    <form id="budget-form">
        <label>Income: <input type="number" step="0.01" id="income" required></label><br>
        <h2>Expenses</h2>
        <div id="expenses-container"></div>
        <button type="button" onclick="addExpense()">Add Expense</button>
        <br><br>
        <button type="button" onclick="calculateBudget()">Calculate Budget</button>
    </form>

    <table id="expense-table" style="display:none;">
        <tr>
            <th>Category</th>
            <th>Amount</th>
        </tr>
    </table>

    <div id="remaining"></div>

    <script>
        let expenseCount = 0;
        const prefillExpenses = [
            "Home Escrow", "APS Electric", "Phone & Internet", "Tidal Music", "Ink service",
            "Student loan", "Hauled water", "Propane", "Trash", "Groceries", "Gas",
            "Discover card", "Amex", "Capital One", "Entertainment", "Clothes", "Haircut",
            "Save or invest"
        ];

        function addExpense(category = "") {
            const container = document.getElementById('expenses-container');
            const div = document.createElement('div');
            div.className = 'expense-row';
            div.innerHTML = `
                <input type="text" id="category_${expenseCount}" value="${category}" placeholder="Category" required>
                <input type="number" step="0.01" id="amount_${expenseCount}" placeholder="Amount" required>
            `;
            container.appendChild(div);
            expenseCount++;
        }

        function calculateBudget() {
            const income = parseFloat(document.getElementById('income').value);
            const expenses = [];
            let totalExpenses = 0;

            for (let i = 0; i < expenseCount; i++) {
                const category = document.getElementById(`category_${i}`).value;
                const amount = parseFloat(document.getElementById(`amount_${i}`).value);

                if (category && amount) {
                    expenses.push({category, amount});
                    totalExpenses += amount;
                }
            }

            const remainingIncome = income - totalExpenses;

            // Update the table
            const table = document.getElementById('expense-table');
            table.style.display = 'table';
            // Clear previous rows
            while (table.rows.length > 1) {
                table.deleteRow(1);
            }

            expenses.forEach(expense => {
                const row = table.insertRow();
                row.insertCell(0).textContent = expense.category;
                row.insertCell(1).textContent = `$${expense.amount.toFixed(2)}`;
            });

            // Update remaining income
            document.getElementById('remaining').textContent = `Remaining to Budget: $${remainingIncome.toFixed(2)}`;
        }

        // Add prefilled expenses
        prefillExpenses.forEach(expense => addExpense(expense));
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
