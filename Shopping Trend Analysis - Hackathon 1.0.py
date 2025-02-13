#!/usr/bin/env python
# coding: utf-8

#                                     Event Name: DatalytiX 1.0

# #1 Problem Statement: Retail businesses often struggle to deeply understand consumer purchasing behaviors and identify actionable patterns that drive profitability and customer satisfaction. With diverse transactional data spanning product categories, customer demographics, and shopping channels, retailers need an analytical approach to uncover trends and behaviors that can guide data-driven decision-making. How can we leverage this dataset to extract insights that optimize marketing strategies, improve customer retention, and maximize revenue?
# 
# Objective: To analyze consumer shopping trends and behaviors through detailed transactional data. The goal is to uncover actionable insights into purchasing patterns, customer preferences, and seasonal trends, enabling retailers to:
# 
# 1) Enhance Marketing Strategies: Identify high-value customer segments and tailor promotions to their preferences.
# 
# 2) Boost Customer Retention: Understand loyalty patterns and develop personalized engagement strategies.
# 
# 3) Optimize Inventory Management: Forecast demand trends across product categories and seasons.
# 
# 4) Improve Channel Performance: Analyze purchase behavior across different channels to prioritize investments in high-performing platforms.
# 
# 5) Visualization: Create impactful visualizations that communicate all findings effectively, supporting data-driven decisions.
# 
# Dataset: shopping_trends
# 

# 1. Enhance Marketing Strategies: Identify high-value customer segments and tailor promotions to their preferences.

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df = pd.read_excel(r"C:\Users\palla\OneDrive\Documents\Dataset_for_DA_Projects\Hackathon 1.0\Shopping_trends.xlsx")


# In[5]:


df.isna().sum()


# In[6]:


numerical_stats = df[["Age", "Purchase Amount (USD)", "Review Rating", "Previous Purchases"]].describe()
numerical_stats


# In[13]:


categorical_columns = ["Gender", "Category", "Season", "Subscription Status", "Payment Method", "Shipping Type"]
for col in categorical_columns:
    print(f"Value counts for {col}:\n", df[col].value_counts(), "\n")


# #Step 1: Identify High-Value Customer Segments
# Definition: High-value customers are those who contribute significantly to revenue or show high purchasing potential.
# 
# Metrics to Analyze:
# a.Total Spending: Customers spending the most.
# b.Frequency of Purchases: Customers making frequent purchases.
# c.Preferred Categories: Popular product categories among high spenders.
# d.Demographics: Age, gender, or location of high-value customers

# In[7]:


# Calculate total spending per customer
customer_spending = df.groupby("Customer ID")["Purchase Amount (USD)"].sum().sort_values(ascending=False)

# Frequent purchasers
customer_frequency = df["Customer ID"].value_counts()

# Merge spending and frequency for comprehensive analysis
customer_analysis = pd.DataFrame({
    "Total Spending (USD)": customer_spending,
    "Purchase Frequency": customer_frequency
}).sort_values(by="Total Spending (USD)", ascending=False)

print(customer_analysis.head(10))  # Top 10 high-value customers


# #Step 2: Analyze Customer Preferences
# #Definition: Uncover trends in what high-value customers prefer (e.g., categories, payment methods, etc.).

# In[8]:


# Filter high-value customers (e.g., top 20% spenders)
top_customers = customer_analysis[customer_analysis["Total Spending (USD)"] > customer_analysis["Total Spending (USD)"].quantile(0.8)]

# Preferences among high-value customers
high_value_preferences = df[df["Customer ID"].isin(top_customers.index)]

# Popular categories
category_preference = high_value_preferences["Category"].value_counts()
print("Top Categories:\n", category_preference)

# Preferred payment methods
payment_preference = high_value_preferences["Payment Method"].value_counts()
print("Preferred Payment Methods:\n", payment_preference)


# #Step 3: Analyze Seasonal Trends
# #Definition: Understand how purchasing patterns vary by season to design seasonal promotions.

# In[10]:


# Seasonal analysis of spending
seasonal_spending = df.groupby("Season")["Purchase Amount (USD)"].mean()

# Seasonal category preferences
seasonal_category = df.groupby(["Season", "Category"])["Purchase Amount (USD)"].sum().unstack()

print("Seasonal Spending:\n", seasonal_spending)
print("\nSeasonal Category Trends:\n", seasonal_category)

# Visualization of seasonal spending
seasonal_spending.plot(kind='bar', color='orange', title="Average Spending by Season")
plt.xlabel("Season")
plt.ylabel("Average Purchase Amount (USD)")
plt.show()

# Heatmap for seasonal category trends
sns.heatmap(seasonal_category, annot=True, cmap="YlGnBu", fmt=".0f")
plt.title("Seasonal Spending by Category")
plt.show()


# Insights to Derive:
# 
# 1.Create exclusive promotions for top categories like "Clothing" during winter and spring
# 
# 2.Incentivize high-value customers with loyalty rewards to boost retention.

# 2. Boost Customer Retention: Understand loyalty patterns and develop personalized engagement strategies.

# Step 1: Analyze Customer Loyalty Patterns
# Definition: Loyalty can be inferred from metrics like subscription status, purchase frequency, and consistency in spending.

# In[13]:


subscription_loyalty = df["Subscription Status"].value_counts(normalize=True) * 100
print("Subscription Status Breakdown (%):\n", subscription_loyalty)

# Analyze purchase frequency by subscription status
freq_by_subscription = df.groupby("Subscription Status")["Frequency of Purchases"].value_counts()
print("\nPurchase Frequency by Subscription Status:\n", freq_by_subscription)

# Spending patterns by subscription
spending_by_subscription = df.groupby("Subscription Status")["Purchase Amount (USD)"].mean()
print("\nAverage Spending by Subscription Status:\n", spending_by_subscription)


# Key Insights-
# 
# 1. Revenue Contribution
# Subscribers: 
# Likely to contribute more to total revenue due to recurring purchases or higher loyalty.
# Typically spend more per transaction compared to non-subscribers, indicating they value the subscription benefits.
# 
# Non-Subscribers:
# May contribute a significant portion of transactions but with lower average spend.
# Often less frequent buyers, indicating the potential for upselling or subscription conversion.
# 
# # Actionable Insight: Focus marketing efforts on converting high-spending non-subscribers into subscribers by emphasizing the value of subscription benefits (e.g., discounts, priority services).
# 
# 2. Purchase Frequency
# Subscribers:
# Likely to purchase more frequently, as subscription models encourage consistent buying.
# Show predictable purchase patterns, such as weekly or monthly shopping habits.
# 
# Non-Subscribers:
# Less predictable purchase behavior, with sporadic or seasonal buying.
# May primarily shop during promotions or discounts.
# Actionable Insight:
# 
# # Develop targeted promotions for non-subscribers to encourage repeat purchases and increase their lifetime value.
# # For subscribers, reinforce loyalty through exclusive offers and early access to new products.

# #Step 2: Identify High-Retention Segments
# #Definition: Customer segments with high engagement and spending potential.

# In[15]:


# Calculate average purchases and spending per frequency group
freq_spending = df.groupby("Frequency of Purchases")["Purchase Amount (USD)"].mean()
freq_spending_count = df["Frequency of Purchases"].value_counts()

print("Average Spending by Frequency of Purchases:\n", freq_spending)
print("\nFrequency of Purchases Count:\n", freq_spending_count)

# Retention by demographic groups (e.g., Age, Gender)
age_retention = df.groupby(pd.cut(df['Age'], bins=[0, 25, 45, 65, 100]))["Purchase Amount (USD)"].mean()
gender_retention = df.groupby("Gender")["Purchase Amount (USD)"].mean()

print("\nRetention by Age Group:\n", age_retention)
print("\nRetention by Gender:\n", gender_retention)


# In[17]:


# Tailor offers to frequent and loyal customers
loyal_customers = df[(df["Subscription Status"] == "Yes") & (df["Frequency of Purchases"].isin(["Weekly", "Fortnightly"]))]

# Preferred categories among loyal customers
loyal_category_preference = loyal_customers["Category"].value_counts()
print("Preferred Categories by Loyal Customers:\n", loyal_category_preference)

# Preferred payment methods among loyal customers
loyal_payment_preference = loyal_customers["Preferred Payment Method"].value_counts()
print("\nPreferred Payment Methods by Loyal Customers:\n", loyal_payment_preference)


# Step 3: Retention Visualization

# In[18]:


# Visualize subscription impact
subscription_loyalty.plot(kind="pie", autopct='%1.1f%%', title="Subscription Status Distribution")
plt.ylabel("")
plt.show()


# In[19]:


# Spending patterns by frequency
freq_spending.plot(kind="bar", color="teal", title="Average Spending by Purchase Frequency")
plt.xlabel("Frequency of Purchases")
plt.ylabel("Average Spending (USD)")
plt.show()


# Insights to Guide Retention Strategies:
# 
# a.Reward Loyalty:
# Offer exclusive discounts to frequent buyers.
# Create a tiered reward system for subscribers.
# 
# b.Personalized Offers:
# Perform promotions based on preferred categories or payment methods.
# Send personalized emails with product recommendations based on purchase history.
# 
# c.High-Retention Segments:
# Focus on demographics (age group of 0-25) or purchase frequencies linked to higher spending like annually.

# 3. Optimize Inventory Management: Forecast demand trends across product categories and seasons.

# #Step 1: Analyze Seasonal Demand Trends
# #Objective: Understand how demand varies across seasons for different product categories.

# In[20]:


# Group data by season and category to analyze demand trends
seasonal_category_demand = df.groupby(["Season", "Category"])["Purchase Amount (USD)"].sum().unstack()

print("Seasonal Demand Trends:\n", seasonal_category_demand)

# Visualize demand trends by season
seasonal_category_demand.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.title("Seasonal Demand by Product Category")
plt.xlabel("Season")
plt.ylabel("Total Purchase Amount (USD)")
plt.legend(title="Category", bbox_to_anchor=(1.05, 1))
plt.show()


# #Step 2: Identify High-Demand Categories
# #Objective: Find categories with the highest total sales and contribution to revenue.

# In[21]:


# Total sales by category
category_sales = df.groupby("Category")["Purchase Amount (USD)"].sum().sort_values(ascending=False)

print("Total Sales by Category:\n", category_sales)

# Visualize top categories
category_sales.plot(kind='bar', color='skyblue', title="Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Purchase Amount (USD)")
plt.show()


# #Step 3: Insights for Inventory Optimization
# 
# a. Seasonal Peaks: Allocate higher inventory for categories like "Clothing" during Winter and spring because sales spike during that season.
# 
# b. Category Trends: Maintain consistent stock for top-performing categories like Clothing across all seasons.
#     
# c. Actionable Inventory Planning: Replenish stocks just before seasonal peaks.

# In[ ]:


#Step 4: Deep Dive into Color and Size Preferences
#Objective: Understand demand patterns for specific product attributes.


# In[29]:


# Popular sizes by category
size_demand = df.groupby(["Category", "Size"])["Purchase Amount (USD)"].sum().unstack()
print("Size Demand by Category:\n", size_demand)

# Popular colors by category
color_demand = df.groupby(["Category", "Color"])["Purchase Amount (USD)"].sum().unstack()
print("Color Demand by Category:\n", color_demand)


# #Insights: 
# 
# 1.Attribute Preferences: Stock popular sizes and colors to avoid unsold inventory.

# In[31]:


size_demand.plot(kind='bar', colormap='Set1')
plt.title('Color Preferences')
plt.xlabel('Color')
plt.ylabel('Frequency')
plt.show()


# 

# In[ ]:




