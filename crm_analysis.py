import pandas as pd

# Load the CRM dataset
df = pd.read_csv("Data/crm_customer_data.csv")

# Display the first 5 rows
print(df.head(5))

# Dataset shape
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Statistical summary of numerical columns
print("\nStatistical Summary:")
print(df.describe())

# Check for duplicate customers
print("\nDuplicate Customer IDs:")
print(df["Customer_ID"].duplicated().sum())

# Check for completely duplicated rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Missing value percentage
print("\nMissing Value Percentage:")
print((df.isnull().sum() / len(df) * 100).round(2))

# Handle missing categorical values
df["Gender"] = df["Gender"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")
df["Product_Category"] = df["Product_Category"].fillna("Unknown")

# Check missing values again
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Convert date columns to datetime
df["Signup_Date"] = pd.to_datetime(df["Signup_Date"])
df["Last_Purchase_Date"] = pd.to_datetime(df["Last_Purchase_Date"])

# Check the data types
print("\nData Types After Date Conversion:")
print(df.dtypes)

# Calculate customer recency
analysis_date = pd.Timestamp("2026-10-01")

df["Recency_Days"] = (
    analysis_date - df["Last_Purchase_Date"]
).dt.days

# Display sample results
print("\nCustomer Recency:")
print(df[["Customer_ID", "Last_Purchase_Date", "Recency_Days"]].head(10))

# Create RFM components
df["Frequency"] = df["Total_Purchases"]
df["Monetary"] = df["Total_Spending"]

# Display RFM components
print("\nRFM Components:")
print(
    df[
        [
            "Customer_ID",
            "Recency_Days",
            "Frequency",
            "Monetary"
        ]
    ].head(10)
)

# Summary of RFM metrics
print("\nRFM Summary:")
print(df[["Recency_Days", "Frequency", "Monetary"]].describe())

# Create RFM scores using quartiles
df["Recency_Score"] = pd.qcut(
    df["Recency_Days"],
    4,
    labels=[4, 3, 2, 1]
).astype(int)

df["Frequency_Score"] = pd.qcut(
    df["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

df["Monetary_Score"] = pd.qcut(
    df["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

# Calculate overall RFM score
df["RFM_Score"] = (
    df["Recency_Score"]
    + df["Frequency_Score"]
    + df["Monetary_Score"]
)

print("\nRFM Scores:")
print(
    df[
        [
            "Customer_ID",
            "Recency_Score",
            "Frequency_Score",
            "Monetary_Score",
            "RFM_Score"
        ]
    ].head(10)
)

# Create customer segments
def assign_segment(row):
    if row["RFM_Score"] >= 10:
        return "High Value"
    elif row["Frequency_Score"] >= 3 and row["Monetary_Score"] >= 3:
        return "Loyal Customers"
    elif row["Recency_Score"] >= 3 and row["Frequency_Score"] >= 2:
        return "Potential Loyalists"
    elif row["Recency_Score"] <= 2:
        return "At Risk"
    else:
        return "Low Value"


df["Customer_Segment"] = df.apply(assign_segment, axis=1)

# Display sample segments
print("\nCustomer Segments:")
print(
    df[
        [
            "Customer_ID",
            "RFM_Score",
            "Customer_Segment"
        ]
    ].head(15)
)

# Count customers in each segment
print("\nCustomer Segment Distribution:")
print(df["Customer_Segment"].value_counts())

# Calculate key CRM KPIs
total_customers = df["Customer_ID"].nunique()
total_revenue = df["Total_Spending"].sum()
total_purchases = df["Total_Purchases"].sum()
average_spending = df["Total_Spending"].mean()

high_value_customers = (
    df["Customer_Segment"] == "High Value"
).sum()

at_risk_customers = (
    df["Customer_Segment"] == "At Risk"
).sum()

print("\nCRM KPIs")
print("-" * 30)
print(f"Total Customers: {total_customers:,}")
print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Purchases: {total_purchases:,}")
print(f"Average Customer Spending: Rs. {average_spending:,.2f}")
print(f"High Value Customers: {high_value_customers:,}")
print(f"At Risk Customers: {at_risk_customers:,}")

import matplotlib.pyplot as plt
import seaborn as sns

# Customer Segment Distribution
segment_counts = df["Customer_Segment"].value_counts()

plt.figure(figsize=(10, 6))

sns.barplot(
    x=segment_counts.index,
    y=segment_counts.values
)

plt.title("Customer Segment Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("charts/customer_segment_distribution.png")

plt.show()

# Revenue by Customer Segment

segment_revenue = (
    df.groupby("Customer_Segment")["Total_Spending"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=segment_revenue.index,
    y=segment_revenue.values
)

plt.title("Revenue by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Revenue (Rs.)")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("charts/revenue_by_customer_segment.png")

plt.show()

# Revenue by Product Category

category_revenue = (
    df.groupby("Product_Category")["Total_Spending"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=category_revenue.index,
    y=category_revenue.values
)

plt.title("Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue (Rs.)")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("charts/revenue_by_product_category.png")

plt.show()

# Revenue by Acquisition Channel

channel_revenue = (
    df.groupby("Acquisition_Channel")["Total_Spending"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=channel_revenue.index,
    y=channel_revenue.values
)

plt.title("Revenue by Acquisition Channel")
plt.xlabel("Acquisition Channel")
plt.ylabel("Total Revenue (Rs.)")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("charts/revenue_by_acquisition_channel.png")

plt.show()

# Customer Status Distribution

status_counts = df["Customer_Status"].value_counts()

plt.figure(figsize=(10, 6))

sns.barplot(
    x=status_counts.index,
    y=status_counts.values
)

plt.title("Customer Status Distribution")
plt.xlabel("Customer Status")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig("charts/customer_status_distribution.png")

plt.show()

# Top 10 Customers by Lifetime Value

top_customers = (
    df.groupby("Customer_ID")["Total_Spending"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=top_customers.values,
    y=top_customers.index
)

plt.title("Top 10 Customers by Lifetime Value")
plt.xlabel("Total Spending (Rs.)")
plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig("charts/top_10_customers_clv.png")

plt.show()

# Save cleaned dataset for dashboard

df.to_csv(
    "output/cleaned_crm_data.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")