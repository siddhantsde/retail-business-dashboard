import pandas as pd
import numpy as np
import random
from datetime import datetime

np.random.seed(100)

start_date = datetime(2026, 3, 1)
dates = pd.date_range(start_date, periods=31)

# Better supplier pricing (healthy margins)
categories = {
    "Grocery": [
        ("Rice 5kg", 320, 260),
        ("Oil 1L", 150, 115),
        ("Wheat Flour 5kg", 280, 220),
        ("Milk 1L", 50, 35)
    ],
    "Snacks": [
        ("Chips Box", 120, 85),
        ("Biscuits Carton", 300, 210)
    ],
    "Personal Care": [
        ("Shampoo", 180, 130),
        ("Soap Pack", 200, 150)
    ],
    "Household": [
        ("Detergent 2kg", 400, 300),
        ("Floor Cleaner", 250, 180)
    ]
}

rows = []
invoice = 1

for date in dates:

    # Higher footfall and weekend spike
    if date.weekday() >= 5:
        transactions = np.random.randint(15, 20)
    else:
        transactions = np.random.randint(12, 16)

    for _ in range(transactions):

        category = random.choices(
            population=list(categories.keys()),
            weights=[55, 20, 15, 10]
        )[0]

        product = random.choice(categories[category])

        quantity = np.random.randint(2, 6)

        # Controlled discount strategy
        discount = random.choice([5, 10, 15])

        rows.append([
            date,
            f"INV{invoice:05d}",
            category,
            product[0],
            quantity,
            product[1],
            product[2],
            discount,
            random.choice(["Cash", "UPI", "Card"]),
            random.choice(["Regular", "Member"]),
            random.choice(["Offline", "Online"])
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

df.to_csv("sales_march_2026_good.csv", index=False)

print("Dataset Generated Successfully!")
print("Total Revenue:", round(df["Revenue"].sum(),2))
print("Total Profit:", round(df["Profit"].sum(),2))
print("Profit Margin %:", round((df["Profit"].sum()/df["Revenue"].sum())*100,2))