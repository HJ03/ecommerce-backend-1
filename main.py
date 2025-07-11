from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Mount static files at /static instead of /
app.mount("/static", StaticFiles(directory="static"), name="static")

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    category: str
    in_stock: bool

products = [
    Product(id=1, name="Laptop", price=50000, description="15-inch Full HD Laptop", category="Electronics", in_stock=True),
    Product(id=2, name="Shoes", price=2500, description="Comfortable running shoes", category="Footwear", in_stock=True),
    Product(id=3, name="Smartphone", price=22000, description="6.5-inch display with 5G support", category="Electronics", in_stock=True),
    Product(id=4, name="Backpack", price=1500, description="Waterproof travel backpack", category="Accessories", in_stock=False),
    Product(id=5, name="Watch", price=3000, description="Stylish digital watch", category="Accessories", in_stock=True),
    Product(id=6, name="T-Shirt", price=700, description="Cotton round neck T-shirt", category="Fashion", in_stock=True),
    Product(id=7, name="Wireless Earbuds", price=1800, description="Bluetooth 5.0 with noise cancellation", category="Electronics", in_stock=True),
    Product(id=8, name="Sunglasses", price=1200, description="UV protection sunglasses", category="Accessories", in_stock=False),
    Product(id=9, name="Gaming Mouse", price=950, description="Ergonomic RGB gaming mouse", category="Electronics", in_stock=True),
    Product(id=10, name="Notebook", price=150, description="A5 size ruled notebook (100 pages)", category="Stationery", in_stock=True)
]

@app.get("/")
def read_index():
    return FileResponse("static/index.html")

@app.get("/products", response_model=List[Product])
def get_products():
    return products
