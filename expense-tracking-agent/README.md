# Expense tracking agent

This is essentially an information retrieval agent. It parses an invoice and extract some useful information. Subsequently, this information are structured and then saved in a database via API routes.

## Tools used
- Langgraph
- FastAPI
- Postgres

## Setup
1. Create a database with the name `expense_tracker_agent_db`.
2. Run the following to create 3 tables(categories, payment_methods and expenses).
```
python src/database/create_tables.py
```
3. Run the following to start up FastAPI server with reloading capability.
```
uvicorn src.api.run_api:app --reload
```
4. Run the following Load the `categories` and `payment_methods` with data in `config.yml` file in the root folder.
```
python src/database/save_categories_and_payment_methods_to_db.py
```