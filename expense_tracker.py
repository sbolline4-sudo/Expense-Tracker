import sqlite3

class ExpenseTracker:

    def __init__(self):
        self.connection = sqlite3.connect("expense.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT
            )
        """)

        self.connection.commit()

    def add_transaction(self):
        while True:
            transaction_type = input("Enter transaction type (income/expense): ").lower()

            if transaction_type == 'income' or transaction_type == 'expense':
                break
            print("Invalid Transaction Type. Please enter Income or Expense.")

        while True:
            try:
                amount = float(input("Enter amount: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break

            except ValueError:
                print("Invalid amount. Please enter a amount.")

        while True:
            category = input("Enter category: ").strip()

            if category:
                break
            print("Category cannot be empty.")

        description = input("Enter description: ").strip()

        self.cursor.execute("""
            INSERT INTO transactions
            (type, amount, category, description)
            VALUES (?, ?, ?, ?)
        """, (transaction_type, amount, category, description))

        self.connection.commit()

        print("Transaction added successfully!")

    def view_transactions(self):
        self.cursor.execute("SELECT * FROM transactions")

        transactions = self.cursor.fetchall()
        if not transactions:
            print("\nNo transactions found.")
            return

        print("\n===== TRANSACTIONS =====\n")
        print(f'{"ID":<5}{"TYPE":<12}{"AMOUNT":<12}{"CATEGORY":<15}{"DESCRIPTION"}')
        print("-" * 60)
        for transaction in transactions:
            transaction_id, transaction_type, amount, category, description = transaction

            print(
                f"{transaction_id:<5}"
                f"{transaction_type:<12}"
                f"{amount:<12.2f}"
                f"{category:15}"
                f"{description or ''}"
            )

    def update_transaction(self):
        while True:

            try:
                transaction_id = int(input("Enter the id: "))

                if transaction_id > 0:
                    break
                print("ID should be greater than 0.")

            except ValueError:
                print("Enter an valid ID.")

        while True:
            transaction_type = input("Enter the new type (income/expense): ").lower()

            if transaction_type == "income" or transaction_type == "expense":
                break
            print("Invalid Transaction type. Enter Income or Expense.")

        while True:
            try:
                amount = float(input("Enter the new amount: "))

                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break

            except ValueError:
                print("Invalid amount. Please enter s amount.")

        while True:
            category = input("Enter new category: ").strip()

            if category:
                break
            print("Category cannot be empty.")

        description = input("Enter the new description: ").strip()

        self.cursor.execute("""
            UPDATE transactions
            SET type = ?, amount = ?, category = ?, description = ?
            WHERE id = ?""", (transaction_type, amount, category, description, transaction_id))
        self.connection.commit()

        if self.cursor.rowcount == 0:
            print("Transaction not found.")
        else:
            print("Transaction Updated Successfully!")

    def delete_transaction(self):
        while True:
            try:
                transaction_id = int(input("Enter the id: "))

                if transaction_id > 0:
                    break
                print("ID cannot be less than 0.")

            except ValueError:
                print("Enter an Valid ID.")

        self.cursor.execute("""
            DELETE FROM transactions
            WHERE id = ?""", (transaction_id,))
        self.connection.commit()

        if self.cursor.rowcount == 0:
            print("Transaction not found.")
        else:
            print("Transaction deleted successfully!")

    def view_balance(self):
        self.cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END),
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END)
        FROM transactions""")

        result = self.cursor.fetchone()

        total_income = result[0] or 0
        total_expense = result[1] or 0
        balance = total_income - total_expense

        print("\n===== BALANCE =====")
        print(f"Total Income: {total_income:.2f}\n"
            f"Total Expense: {total_expense:.2f}\n"
            f"Balance: {balance:.2f}")

    def close(self):
        self.connection.close()

tracker = ExpenseTracker()

while True:

    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Transaction.")
    print("2. View Transactions.")
    print("3. Update Transaction.")
    print("4. Delete Transaction.")
    print("5. View Balance.")
    print("6. Exit.")

    choice = input("Enter your choice: ")

    if choice == "1":
        tracker.add_transaction()
    elif choice == "2":
        tracker.view_transactions()

    elif choice == "3":
        tracker.update_transaction()

    elif choice == "4":
        tracker.delete_transaction()

    elif choice == "5":
        tracker.view_balance()

    elif choice == "6":
        print("Goodbye!")
        tracker.close()
        break

    else:
        print("Invalid choice. Please try again.")