from database import SessionLocal, engine
from models import Product, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Sample products to insert
sample_products = [
    Product(name="Laptop", price=50000, description="15-inch Full HD Laptop", category="Electronics", in_stock=True),
    Product(name="Shoes", price=2500, description="Comfortable running shoes", category="Footwear", in_stock=True),
    Product(name="Smartphone", price=22000, description="6.5-inch display with 5G support", category="Electronics", in_stock=True),
    Product(name="Backpack", price=1500, description="Waterproof travel backpack", category="Accessories", in_stock=False),
    Product(name="Watch", price=3000, description="Stylish digital watch", category="Accessories", in_stock=True),
    Product(name="T-Shirt", price=700, description="Cotton round neck T-shirt", category="Fashion", in_stock=True),
    Product(name="Wireless Earbuds", price=1800, description="Bluetooth 5.0 with noise cancellation", category="Electronics", in_stock=True),
    Product(name="Sunglasses", price=1200, description="UV protection sunglasses", category="Accessories", in_stock=False),
    Product(name="Gaming Mouse", price=950, description="Ergonomic RGB gaming mouse", category="Electronics", in_stock=True),
    Product(name="Notebook", price=150, description="A5 size ruled notebook (100 pages)", category="Stationery", in_stock=True),
    
    # ✅ NEW PRODUCTS
    Product(name="Desk Lamp", price=850, description="LED desk lamp with brightness control", category="Home", in_stock=True),
    Product(name="Office Chair", price=7500, description="Ergonomic mesh office chair", category="Furniture", in_stock=True),
    Product(name="Power Bank", price=1600, description="10,000mAh portable charger", category="Electronics", in_stock=True),
    Product(name="Bluetooth Speaker", price=2200, description="Portable speaker with 10hr battery", category="Electronics", in_stock=True),
    Product(name="Fitness Band", price=2999, description="Track steps, sleep, and heart rate", category="Fitness", in_stock=True),
]


# Create a database session
db = SessionLocal()

# Add this before the insertion block
db.query(Product).delete()
db.commit()

# Insert data only if the table is empty
if db.query(Product).count() == 0:
    db.add_all(sample_products)
    db.commit()
    print("✅ Sample products inserted successfully.")
else:
    print("ℹ️ Products already exist. No new products were inserted.")

db.close()
