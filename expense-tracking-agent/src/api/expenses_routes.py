from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, validator
from src.database.db_connection import conn, cursor
from dotenv import load_dotenv
from datetime import date
from decimal import Decimal
import psycopg2

load_dotenv()

class ExpenseCreate(BaseModel):
    date: date
    category_id: int
    description: str
    amount: Decimal 
    vat: Decimal 
    payment_method_id: int 
    business_personal: str

    @validator("date")
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("Date cannot be in the future")
        return value

class ExpenseDelete(BaseModel):
    transaction_id: int

class Expense(BaseModel):
    transaction_id: int
    date: date
    category_id: int
    description: str
    amount: Decimal
    vat: Decimal
    payment_method_id: int
    business_personal: str


# Initialize APIRouter
router = APIRouter()

# GET all expenses with optional filters
@router.get("/expenses", response_model=list[Expense])
def get_expenses(
    category_id: int = None,
    payment_method_id: int = None,
    start_date: date = None, 
    end_date: date = None):
    try:
        # Construct SQL query
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if category_id is not None:
            query += " AND category_id = %s"
            params.append(category_id)

        if payment_method_id is not None:
            query += " AND payment_method_id = %s"
            params.append(payment_method_id)

        if start_date is not None:
            query += " AND date >= %s"
            params.append(start_date)

        if end_date is not None:
            query += " AND date <= %s"
            params.append(end_date)

        cursor.execute(query, tuple(params))
        expenses = cursor.fetchall()

        if not expenses:
            raise HTTPException(status_code=404, detail="No expenses found for the given filters")

        return [Expense(transaction_id=expense[0], date=expense[1], category_id=expense[2], description=expense[3],
                        amount=expense[4], vat=expense[5], payment_method_id=expense[6], business_personal=expense[7]) for expense in expenses]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST an expense
@router.post("/expenses", response_model=Expense)
def create_expense(expense_data: ExpenseCreate):
    try:
        cursor.execute(
            "INSERT INTO expenses (date, category_id, description, amount, vat, payment_method_id, business_personal) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id, date, category_id, description, amount, vat, payment_method_id, business_personal",
            (expense_data.date, expense_data.category_id, expense_data.description, expense_data.amount, expense_data.vat, expense_data.payment_method_id, expense_data.business_personal)
        )
        new_expense = cursor.fetchone()
        conn.commit()
        return Expense(transaction_id=new_expense[0], date=new_expense[1], category_id=new_expense[2], description=new_expense[3],
                       amount=new_expense[4], vat=new_expense[5], payment_method_id=new_expense[6], business_personal=new_expense[7])
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# DELETE an expense
@router.delete("/expenses")
def delete_expense(expense_data: ExpenseDelete):
    try:
        cursor.execute("DELETE FROM expenses WHERE transaction_id = %s RETURNING transaction_id", (expense_data.transaction_id,))
        deleted_expense = cursor.fetchone()
        if not deleted_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        conn.commit()
        return {"message": "Expense deleted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")