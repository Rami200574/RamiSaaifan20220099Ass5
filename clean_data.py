import pandas as pd

# Load the raw CSV file with all columns as strings
df = pd.read_csv('ebay_tech_deals.csv', dtype=str)

# Clean the 'price' and 'original_price' columns
df['price'] = df['price'].str.replace('US \$', '', regex=True)  # Remove 'US $'
df['price'] = df['price'].str.replace(',', '', regex=True)  # Remove commas
df['price'] = df['price'].str.strip()  # Trim extra whitespace

df['original_price'] = df['original_price'].str.replace('US \$', '', regex=True)  # Remove 'US $'
df['original_price'] = df['original_price'].str.replace(',', '', regex=True)  # Remove commas
df['original_price'] = df['original_price'].str.strip()  # Trim extra whitespace

# If 'original_price' is missing (i.e., marked as 'N/A' or empty), replace it with the corresponding price
df['original_price'] = df['original_price'].replace(['N/A', ''], pd.NA)
df['original_price'] = df['original_price'].fillna(df['price'])

# Clean the 'shipping' column by replacing "N/A", empty strings, or strings containing only whitespace with the default message
df['shipping'] = df['shipping'].replace(['N/A', '', ' '], 'Shipping info unavailable')

# Convert 'price' and 'original_price' columns to numeric (float) values
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce')

# Create a new column 'discount_percentage' calculated as: 
# (original_price - price) / original_price * 100
df['discount_percentage'] = ((df['original_price'] - df['price']) / df['original_price']) * 100

# Round 'discount_percentage' to two decimal places
df['discount_percentage'] = df['discount_percentage'].round(2)

# Save the cleaned data as 'cleaned_ebay_deals.csv'
df.to_csv('cleaned_ebay_deals.csv', index=False)

print("Data cleaning completed and saved to 'cleaned_ebay_deals.csv'.")
