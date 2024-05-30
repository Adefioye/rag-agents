from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from src.database.db_connection import conn, cursor

# Define Pydantic models for request and response
class PaymentMethodCreate(BaseModel):
    payment_method_name: str

class PaymentMethodDelete(BaseModel):
    payment_method_id: int

class PaymentMethod(BaseModel):
    payment_method_id: int
    payment_method_name: str

# Initialize APIRouter
router = APIRouter()

# GET all payment methods
@router.get("/payment_methods", response_model=list[PaymentMethod])
def get_payment_methods():
    try:
        cursor.execute("SELECT payment_method_id, payment_method_name FROM payment_methods")
        payment_methods = cursor.fetchall()
        return [{"payment_method_id": method[0], "payment_method_name": method[1]} for method in payment_methods]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST a payment method
@router.post("/payment_methods", response_model=PaymentMethod)
def create_payment_method(payment_method_data: PaymentMethodCreate):
    try:
        cursor.execute("INSERT INTO payment_methods (payment_method_name) VALUES (%s) RETURNING payment_method_id, payment_method_name", (payment_method_data.payment_method_name,))
        method = cursor.fetchone()
        conn.commit()
        return {"payment_method_id": method[0], "payment_method_name": method[1]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# DELETE a payment method
@router.delete("/payment_methods")
def delete_payment_method(payment_method_data: PaymentMethodDelete):
    try:
        cursor.execute("DELETE FROM payment_methods WHERE payment_method_id = %s RETURNING payment_method_id", (payment_method_data.payment_method_id,))
        deleted_method = cursor.fetchone()
        if not deleted_method:
            raise HTTPException(status_code=404, detail="Payment method not found")
        conn.commit()
        return {"message": "Payment method deleted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")