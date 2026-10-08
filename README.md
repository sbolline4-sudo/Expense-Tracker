# Expense Tracker

A command-line Expense Tracker built with Python and SQLite.

## Features

- Add income and expenses
- View all transactions
- Update transactions
- Delete transactions
- Calculate total income
- Calculate total expenses
- Calculate current balance
- Input validation
- Persistent data storage using SQLite

## Technologies Used

- Python
- SQLite
- Object-Oriented Programming (OOP)
- SQL

## Database

The application uses SQLite for persistent storage.

The database contains a `transactions` table with:

- `id`
- `type`
- `amount`
- `category`
- `description`

The `expense.db` file is created automatically when the application runs.

## How to Run

### 1. Clone the repository

```bash
git clone <https://github.com/sbolline4-sudo/Expense-Tracker>
