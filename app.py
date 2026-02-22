import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(layout="wide")
st.title("General Store Business Dashboard")

# -----------------------------
# Upload Dataset
# -----------------------------
st.sidebar.header("Upload Store Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload your store transaction CSV file.")
    st.stop()

data = pd.read_csv(uploaded_file)
data["Date"] = pd.to_datetime(data["Date"])

# -----------------------------
# Calculated Columns
# -----------------------------
data["Revenue"] = data["Quantity"] * data["Unit_Price"] * (1 - data["Discount"]/100)
data["Profit"] = (data["Unit_Price"] - data["Cost_Price"]) * data["Quantity"]

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Category",
    options=data["Product_Category"].unique(),
    default=data["Product_Category"].unique()
)

store_filter = st.sidebar.multiselect(
    "Store Type",
    options=data["Store_Type"].unique(),
    default=data["Store_Type"].unique()
)

filtered_data = data[
    (data["Product_Category"].isin(category_filter)) &
    (data["Store_Type"].isin(store_filter))
]

# -----------------------------
# Executive Summary
# -----------------------------
st.header("Executive Summary")

total_revenue = filtered_data["Revenue"].sum()
total_profit = filtered_data["Profit"].sum()
total_orders = filtered_data["Invoice_ID"].nunique()
avg_order_value = total_revenue / total_orders if total_orders != 0 else 0
profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", round(total_revenue,2))
col2.metric("Total Profit", round(total_profit,2))
col3.metric("Total Orders", total_orders)
col4.metric("Profit Margin %", round(profit_margin,2))

# -----------------------------
# Performance Overview
# -----------------------------
st.header("Performance Overview")

daily_summary = filtered_data.groupby("Date").agg({
    "Revenue": "sum",
    "Profit": "sum",
    "Invoice_ID": "count"
}).reset_index()

daily_summary.rename(columns={"Invoice_ID": "Orders"}, inplace=True)

colA, colB = st.columns(2)

with colA:
    st.subheader("Daily Revenue Trend")
    fig1 = plt.figure()
    plt.plot(daily_summary["Date"], daily_summary["Revenue"])
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    st.pyplot(fig1)

with colB:
    st.subheader("Daily Profit Trend")
    fig2 = plt.figure()
    plt.plot(daily_summary["Date"], daily_summary["Profit"])
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Profit")
    st.pyplot(fig2)

# -----------------------------
# Category Snapshot
# -----------------------------
st.header("Category Strength & Weakness")

category_revenue = filtered_data.groupby("Product_Category")["Revenue"].sum().sort_values(ascending=False)

st.write("Top Performing Category:", category_revenue.index[0])
st.write("Lowest Performing Category:", category_revenue.index[-1])

category_percentage = (category_revenue / category_revenue.sum()) * 100

st.write("Category Contribution (%)")
st.write(round(category_percentage,2))


# ==================================
# GROWTH ANALYSIS
# ==================================

st.header("Growth Analysis")

if len(daily_summary) >= 10:
    first_half = daily_summary["Revenue"].iloc[:len(daily_summary)//2].mean()
    second_half = daily_summary["Revenue"].iloc[len(daily_summary)//2:].mean()
    
    growth_rate = ((second_half - first_half) / first_half) * 100
    
    st.write("Revenue Growth (First Half vs Second Half):", round(growth_rate,2), "%")
    
    if growth_rate > 5:
        st.success("Business is showing positive growth trend.")
    elif growth_rate < -5:
        st.error("Revenue is declining compared to earlier period.")
    else:
        st.info("Revenue is relatively stable.")

# ==================================
# BUSINESS HEALTH & INSIGHTS
# ==================================

st.header("Business Health Analysis")

# Basic comparisons
recent_revenue = daily_summary["Revenue"].tail(5).mean()
overall_revenue = daily_summary["Revenue"].mean()

recent_orders = daily_summary["Orders"].tail(5).mean()
overall_orders = daily_summary["Orders"].mean()

avg_discount = filtered_data["Discount"].mean()

alerts = []

# Revenue movement
if recent_revenue < overall_revenue * 0.85:
    alerts.append("Sales have dropped in the last few days.")
elif recent_revenue > overall_revenue * 1.10:
    alerts.append("Sales are improving compared to earlier period.")

# Profit condition
if profit_margin < 8:
    alerts.append("Overall profit margin is low.")

# Customer movement
if recent_orders < overall_orders * 0.85:
    alerts.append("Customer footfall has reduced recently.")

# Discount impact
if avg_discount > 20:
    alerts.append("High average discount may be reducing profitability.")

# Category dependency
category_percentage = (category_revenue / category_revenue.sum()) * 100
if category_percentage.max() > 60:
    alerts.append("Revenue is heavily dependent on one category.")

# Display alerts
if len(alerts) == 0:
    st.success("Business performance is stable. No major risks detected.")
else:
    for a in alerts:
        st.warning(a)


# ==================================
# PROFIT QUALITY ANALYSIS
# ==================================

st.header("Profit Quality Analysis")

high_discount_sales = filtered_data[filtered_data["Discount"] > 25]["Revenue"].sum()
total_sales = filtered_data["Revenue"].sum()

discount_dependency = (high_discount_sales / total_sales) * 100 if total_sales != 0 else 0

st.write("Revenue from Heavy Discount Sales:", round(discount_dependency,2), "%")

if discount_dependency > 40:
    st.warning("Large portion of revenue depends on heavy discounts.")
elif discount_dependency < 15:
    st.success("Revenue not heavily dependent on discounts.")
else:
    st.info("Moderate dependency on discount-based sales.")

    
# ==================================
# WHAT TO EXPECT (SHORT FORECAST)
# ==================================

st.header("What To Expect (Next 7 Days)")

daily_summary["Day_Number"] = (
    daily_summary["Date"] - daily_summary["Date"].min()
).dt.days

X = daily_summary[["Day_Number"]]
y = daily_summary["Revenue"]

model = LinearRegression()
model.fit(X, y)

future_day = daily_summary["Day_Number"].max() + 7
predicted_revenue = model.predict([[future_day]])[0]

st.metric("Expected Revenue After 7 Days", round(predicted_revenue, 2))

# ==================================
# ACTION RECOMMENDATIONS
# ==================================

st.header("Recommended Actions for Store Owner")

recommendations = []

if profit_margin < 8:
    recommendations.append("Review supplier pricing or reduce heavy discounts.")

if recent_orders < overall_orders * 0.85:
    recommendations.append("Consider local promotions or marketing to increase footfall.")

if avg_discount > 20:
    recommendations.append("Re-evaluate discount strategy and check if it increases volume enough.")

if category_percentage.max() > 60:
    recommendations.append("Increase focus on weaker categories to balance revenue.")

if recent_revenue < overall_revenue * 0.85:
    recommendations.append("Run short-term offers to boost immediate sales.")

if len(recommendations) == 0:
    st.write("Current strategy looks healthy. Maintain consistency.")
else:
    for r in recommendations:
        st.write("- " + r)

# ==================================
# OVERALL BUSINESS RISK SCORE
# ==================================

st.header("Overall Business Score")

risk_points = 0

if profit_margin < 8:
    risk_points += 1

if avg_discount > 25:
    risk_points += 1

if recent_revenue < overall_revenue * 0.85:
    risk_points += 1

if recent_orders < overall_orders * 0.85:
    risk_points += 1

score = 100 - (risk_points * 20)

st.metric("Business Health Score (Out of 100)", score)

if score >= 80:
    st.success("Business performance is strong.")
elif score >= 60:
    st.info("Business is stable but needs attention in some areas.")
else:
    st.error("Business performance is at risk. Immediate action required.")