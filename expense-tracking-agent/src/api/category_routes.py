from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from src.database.db_connection import conn, cursor

# Define Pydantic models for request and response
class CategoryCreate(BaseModel):
    category_name: str

class CategoryDelete(BaseModel):
    category_name: str

class Category(BaseModel):
    category_id: int
    category_name: str

# Helper function to close database connection
def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()

# Initialize APIRouter
router = APIRouter()

# GET all categories
@router.get("/categories", response_model=list[Category])
def get_categories():
    try:
        cursor.execute("SELECT category_id, category_name FROM categories")
        categories = cursor.fetchall()
        return [{"category_id": category[0], "category_name": category[1]} for category in categories]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# POST a category
@router.post("/categories", response_model=Category)
def create_category(category_data: CategoryCreate):
    try:
        cursor.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id, category_name", (category_data.category_name,))
        category = cursor.fetchone()
        conn.commit()
        return {"category_id": category[0], "category_name": category[1]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# DELETE a category
@router.delete("/categories")
def delete_category(category_data: CategoryDelete):
    try:
        cursor.execute("DELETE FROM categories WHERE category_name = %s RETURNING category_name", (category_data.category_name,))
        deleted_category = cursor.fetchone()
        if not deleted_category:
            raise HTTPException(status_code=404, detail="Category not found")
        conn.commit()
        return {"message": "Category deleted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")