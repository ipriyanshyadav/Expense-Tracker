import sqlite3
from werkzeug.security import generate_password_hash
import os


def get_db():
    """Opens connection to spendly.db with row_factory and foreign keys enabled"""
    # Get the absolute path to the database file in the project root
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Creates users and expenses tables if they don't exist"""
    conn = get_db()
    try:
        # Create users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Create expenses table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Seeds the database with demo user and sample expenses if not already seeded"""
    conn = get_db()
    try:
        # Check if users table already has data
        cursor = conn.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]

        if user_count > 0:
            # Data already exists, skip seeding
            return

        # Insert demo user
        demo_password_hash = generate_password_hash('demo123')
        cursor = conn.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('Demo User', 'demo@spendly.com', demo_password_hash))
        user_id = cursor.lastrowid

        # Sample expenses data (8 total, covering all categories)
        sample_expenses = [
            (user_id, 12.50, 'Food', '2026-05-01', 'Groceries at local market'),
            (user_id, 8.75, 'Food', '2026-05-03', 'Coffee and pastry'),
            (user_id, 45.00, 'Transport', '2026-05-05', 'Gas refill'),
            (user_id, 89.99, 'Bills', '2026-05-02', 'Electricity bill'),
            (user_id, 25.00, 'Health', '2026-05-04', 'Pharmacy purchase'),
            (user_id, 20.00, 'Entertainment', '2026-05-06', 'Movie tickets'),
            (user_id, 75.50, 'Shopping', '2026-05-01', 'Clothing purchase'),
            (user_id, 10.00, 'Other', '2026-05-02', 'Parking fee'),
        ]

        # Insert sample expenses
        conn.executemany('''
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_expenses)

        conn.commit()
    finally:
        conn.close()