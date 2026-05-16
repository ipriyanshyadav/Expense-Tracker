# Technical Design Document: Database Setup for Spendly Expense Tracker

## Context
This implementation establishes the data layer foundation for the Spendly application as specified in Step 1 of the project roadmap. The database setup must be completed before any authentication, profile, or expense tracking features can function, as all future features depend on this foundation. Currently, `database/db.py` contains only stub comments, and the application lacks persistent data storage.

## Recommended Approach
Implement the three required functions in `database/db.py` following the specifications precisely, then modify `app.py` to import and initialize the database on startup.

### 1. Database Implementation (`database/db.py`)
- **get_db()**: Create SQLite connection to `spendly.db` in project root, set `row_factory = sqlite3.Row`, enable foreign keys with `PRAGMA foreign_keys = ON`, return connection
- **init_db()**: Execute CREATE TABLE IF NOT EXISTS statements for users and expenses tables with exact schema from specs
- **seed_db()**: Check for existing users, insert demo user with hashed password, insert 8 sample expenses across all categories with varied dates

### 2. Application Integration (`app.py`)
- Add imports: `from database.db import get_db, init_db, seed_db`
- Within `app.app_context()`: call `init_db()` then `seed_db()` before first request

## Critical Files to Modify
- `/Users/priyanshyadav/PyCharmMiscProject/Practice/CampusX/Claude Code/expense-tracker/database/db.py` - Implement all three functions
- `/Users/priyanshyadav/PyCharmMiscProject/Practice/CampusX/Claude Code/expense-tracker/app.py` - Add imports and startup calls

## Existing Patterns to Reuse
- Follow the template inheritance pattern seen in `base.html` for consistent structure
- Use `url_for()` for all internal links as demonstrated in existing templates
- Apply parameterized queries as required by project constraints
- Use `werkzeug.security.generate_password_hash` for password hashing (already imported in requirements)

## Verification Plan
1. **Manual Testing**:
   - Start application: `python app.py`
   - Verify database file (`spendly.db`) is created in project root
   - Check that app starts without errors
   - Verify tables exist with correct schema using SQLite CLI or DB browser
   - Confirm demo user exists with hashed password
   - Confirm 8 sample expenses exist across all 7 categories (Food, Transport, Bills, Health, Entertainment, Shopping, Other)
   - Test that repeated runs don't create duplicate seed data
   - Verify foreign key constraints work (attempt to insert expense with invalid user_id should fail)

2. **Automated Testing** (when tests are added):
   - Test `get_db()` returns connection with `row_factory=sqlite3.Row` and foreign keys enabled
   - Test `init_db()` creates tables correctly and is idempotent
   - Test `seed_db()` inserts correct data and prevents duplication
   - Test database enforces UNIQUE constraint on users.email
   - Test database enforces FOREIGN KEY constraint on expenses.user_id

## Implementation Notes
- Use `sqlite3.connect('spendly.db')` or check for existing file patterns
- Store dates in YYYY-MM-DD format as TEXT
- Use REAL type for amount (not INTEGER)
- Ensure `seed_db()` uses exact categories list: Food, Transport, Bills, Health, Entertainment, Shopping, Other
- Spread sample expenses across current month dates
- Hash password "demo123" using `werkzeug.security.generate_password_hash`
- Never use string formatting in SQL - only parameterized queries with `?` placeholders