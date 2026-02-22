import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed
np.random.seed(42)

# Date range for 1 year
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date)

categories = {
    "Electronics": [
        ("Headphones", 1500, 1000),
        ("Mouse", 700, 450),
        ("Keyboard", 1200, 800),
        ("Tablet", 15000, 11000),
        ("Speaker", 4000, 2800)
    ],
    "Clothing": [
        ("T-Shirt", 800, 500),
        ("Jeans", 2500, 1700),
        ("Jacket", 3500, 2500),
        ("Shoes", 3000, 2000),
        ("Shirt", 1200, 800)
    ],
    "Grocery": [
        ("Rice", 60, 40),
        ("Oil", 150, 100),
        ("Milk", 40, 25),
        ("Tea", 200, 120),
        ("Biscuits", 20, 12)
    ]
}

payment_methods = ["Cash", "Card", "UPI"]
customer_types = ["Member", "Regular"]
store_types = ["Online", "Offline"]

rows = []
invoice_counter = 1

for single_date in date_range:
    # Base daily transactions
    transactions = np.random.randint(5, 15)

    # Weekend boost
    if single_date.weekday() >= 5:
        transactions += 5

    # Festival season (Oct–Dec boost)
    if single_date.month in [10, 11, 12]:
        transactions += 5

    for _ in range(transactions):
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        quantity = np.random.randint(1, 5)
        discount = random.choice([0, 5, 10, 15])
        payment = random.choice(payment_methods)
        customer = random.choice(customer_types)
        store = random.choice(store_types)

        rows.append([
            single_date,
            f"INV{invoice_counter:05d}",
            category,
            product[0],
            quantity,
            product[1],
            product[2],
            discount,
            payment,
            customer,
            store
        ])

        invoice_counter += 1

columns = [
    "Date", "Invoice_ID", "Product_Category", "Product_Name",
    "Quantity", "Unit_Price", "Cost_Price", "Discount",
    "Payment_Method", "Customer_Type", "Store_Type"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("retail_data.csv", index=False)

print("1-Year Realistic Retail Dataset Generated Successfully!")