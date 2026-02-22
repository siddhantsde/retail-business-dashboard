import pandas as pd
import numpy as np
import random
from datetime import datetime

np.random.seed(42)

start_date = datetime(2026, 2, 1)
dates = pd.date_range(start_date, periods=28)

# More realistic pricing gap
categories = {
    "Grocery": [
        ("Rice 5kg", 320, 285),
        ("Oil 1L", 150, 130),
        ("Wheat Flour 5kg", 280, 250),
        ("Milk 1L", 50, 42)
    ],
    "Snacks": [
        ("Chips Box", 120, 100),
        ("Biscuits Carton", 300, 260)
    ],
    "Personal Care": [
        ("Shampoo", 180, 155),
        ("Soap Pack", 200, 170)
    ],
    "Household": [
        ("Detergent 2kg", 400, 360),
        ("Floor Cleaner", 250, 220)
    ]
}

rows = []
invoice = 1

for date in dates:

    # Normal days vs weak last week
    if date.day > 21:
        transactions = np.random.randint(6, 9)
    else:
        transactions = np.random.randint(9, 13)

    for _ in range(transactions):

        category = random.choices(
            population=list(categories.keys()),
            weights=[70, 12, 10, 8]
        )[0]

        product = random.choice(categories[category])

        quantity = np.random.randint(1, 4)

        # Moderate discounts (realistic)
        discount = random.choice([5, 10, 15, 20, 25])

        rows.append([
            date,
            f"INV{invoice:04d}",
            category,
            product[0],
            quantity,
            product[1],
            product[2],
            discount,
            random.choice(["Cash", "UPI", "Card"]),
            random.choice(["Regular", "Member"]),
            "Offline"
        ])

        invoice += 1

columns = [
    "Date","Invoice_ID","Product_Category","Product_Name",
    "Quantity","Unit_Price","Cost_Price","Discount",
    "Payment_Method","Customer_Type","Store_Type"
]

df = pd.DataFrame(rows, columns=columns)

df["Revenue"] = df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"]/100)
df["Profit"] = (df["Unit_Price"] - df["Cost_Price"]) * df["Quantity"]

df.to_csv("sales_feb_2026_bad.csv", index=False)

print("Dataset Generated Successfully!")
print("Total Revenue:", round(df["Revenue"].sum(),2))
print("Total Profit:", round(df["Profit"].sum(),2))
print("Profit Margin %:", round((df["Profit"].sum()/df["Revenue"].sum())*100,2))