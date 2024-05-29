from db_connection import conn, cursor

# Define SQL statements to create tables
create_table_categories = """
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE
);
"""

create_table_payment_methods = """
CREATE TABLE payment_methods (
    payment_method_id SERIAL PRIMARY KEY,
    payment_method_name VARCHAR(100) UNIQUE
);
"""

create_table_expenses = """
CREATE TABLE expenses (
    transaction_id SERIAL PRIMARY KEY,
    date DATE,
    category_id INT,
    description TEXT,
    amount DECIMAL(10, 2),
    vat DECIMAL(10, 2),
    payment_method_id INT,
    business_personal VARCHAR(100),
    declared_on DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id)
);
"""

# Execute the SQL statements to create tables
cursor.execute(create_table_categories)
cursor.execute(create_table_payment_methods)
cursor.execute(create_table_expenses)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()