"""The connects to postgres and exposes conn and cursor object
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Establish connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Create a cursor object
cursor = conn.cursor()