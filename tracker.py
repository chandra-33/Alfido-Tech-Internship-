import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER,
    date TEXT,
    category TEXT,
    amount REAL,
    type TEXT
)
''')
conn.commit()
def add_trans(date, category, amount, t_type):
    cursor.execute('''
    INSERT INTO transactions (date, category, amount, type)
    VALUES (?, ?, ?, ?)
    ''', (date, category, amount, t_type))
    conn.commit()
    print("Transaction added successfully!")
def view_trans():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    print(df)
    return df
def generate_rep():
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    if df.empty:
        print("No transactions available to generate a report.")
        return
    income = df[df['type'] == 'Income']['amount'].sum()
    expenses = df[df['type'] == 'Expense']['amount'].sum()
    savings = income - expenses
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${savings:.2f}")
    df_expenses = df[df['type'] == 'Expense']
    if not df_expenses.empty:
        plt.figure(figsize=(8, 5))
        df_expenses.groupby('category')['amount'].sum().plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")
        plt.ylabel("")
        plt.show()

def set_budget(goal_amount):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL
    )
    ''')
    cursor.execute('DELETE FROM budget')
    cursor.execute('INSERT INTO budget (amount) VALUES (?)', (goal_amount,))
    conn.commit()
    print(f"Budget goal of ${goal_amount} set successfully!")
def track_budget_progress():
    cursor.execute('SELECT amount FROM budget')
    budget = cursor.fetchone()
    if not budget:
        print("No budget goal set.")
        return
    budget = budget[0]
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    total_expenses = df[df['type'] == 'Expense']['amount'].sum()
    remaining_budget = budget - total_expenses
    print(f"Budget Goal: ${budget:.2f}")
    print(f"Expenses: ${total_expenses:.2f}")
    print(f"Remaining Budget: ${remaining_budget:.2f}")
    plt.figure(figsize=(6, 4))
    plt.bar(['Spent', 'Remaining'], [total_expenses, remaining_budget], color=['red', 'green'])
    plt.title("Budget Progress")
    plt.ylabel("Amount ($)")
    plt.show()
def export_data_to_csv(file_name='finance_data.csv'):
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    if df.empty:
        print("No data to export.")
        return
    df.to_csv(file_name, index=False)
    print(f"Data exported successfully to {file_name}")
while True:
    print("\n=== Personal Finance Tracker ===")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Generate Report")
    print("4. Set Budget Goal")
    print("5. Track Budget Progress")
    print("6. Export Data to CSV")
    print("7. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        date = input("Enter date (YYYY-MM-DD): ")
        category = input("Enter category (e.g., Rent, Groceries): ")
        amount = float(input("Enter amount: "))
        t_type = input("Enter type (Income/Expense): ")
        add_trans(date, category, amount, t_type)
    elif choice == '2':
        view_trans()
    elif choice == '3':
        generate_rep()
    elif choice == '4':
        goal = float(input("Enter budget goal: "))
        set_budget(goal)
    elif choice == '5':
        track_budget_progress()
    elif choice == '6':
        file_name = input("Enter file name (default: finance_data.csv): ")
        export_data_to_csv(file_name if file_name else 'finance_data.csv')
    elif choice == '7':
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()
