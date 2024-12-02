import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set file path
downloads_folder = os.path.expanduser("~/Downloads")
file_name = "ml.csv"  # Replace with your CSV file name
file_path = os.path.join(downloads_folder, file_name)

# Load CSV file
try:
    data = pd.read_csv(file_path)
    print("Data imported successfully!")
    print(data.shape)  # Show the first 5 rows
except FileNotFoundError:
    print(f"File not found at {file_path}. Please check the file name or path.")


# returing unique values

categorical_columns = data.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    unique_values = data[col]
    print(f"{col}: {len(unique_values.dtypes)} unique values")
    
    
# returing value datatypes
# Displaying data types of each column
print("Data types of each column:")
print(data.dtypes)



# Returning unique values and value counts for categorical columns
categorical_columns = data.select_dtypes(include=["object"]).columns
for col in categorical_columns:
    unique_values = data[col]
    # print(f"{col}: {len(unique_values)} unique values") 
    
    # # Display value counts for each categorical column
    # print(f"Value counts for '{col}':")
    # print(data[col].value_counts())
    # print()
    
    
    
# returing null values , checking for null values
# Checking for null values in the DataFrame before applying forward fill
print("Number of null values in each column before forward fill:")
print(data.isnull().sum())

# Applying forward fill to the DataFrame
data.ffill(inplace=True)

# Verifying that forward fill was applied
print("\nData after forward fill:")
print(data.head())

# Checking for null values in the DataFrame after applying forward fill
print("Number of null values in each column after forward fill:")
print(data.isnull().sum())

# Convert Data Types
# Convert 'selling_price' to float
data['selling_price'] = data['selling_price'].astype(float)

# Convert 'purchase_price' to float with error handling and coercion
data['purchase_price'] = pd.to_numeric(data['purchase_price'], errors='coerce', downcast='float')

# Convert 'purchase_date' to datetime with error handling and coercion
data['purchase_date'] = pd.to_datetime(data['purchase_date'], errors='coerce')

# Display data types after conversion
print("\nData types after conversion:")
print(data.dtypes)

# Plotting code
# plt.figure(figsize=(20, 5))
# sns.countplot(x='manufacturer', data=data.sort_values(by='manufacturer'), hue='manufacturer', palette='husl', legend=False)
# plt.grid(color="green", linestyle="--", linewidth=0.5)
# plt.title("Companies with their sold Vehicles", fontdict={"family": "serif", "color": "blue", "size": 20})
# plt.xticks(rotation=90)  # Rotate x labels for better visibility
# plt.show()

# Data type conversion and forward fill
data['selling_price'] = data['selling_price'].astype(float)
data['purchase_price'] = pd.to_numeric(data['purchase_price'], errors='coerce', downcast='float')
data['purchase_date'] = pd.to_datetime(data['purchase_date'], errors='coerce')
data.ffill(inplace=True)

# Groupby analysis with aggregation
aggregated_data = data.groupby('manufacturer').agg({
    'seating_capacity': ['min', 'max', 'mean', 'std', 'first', 'last'],
    'selling_price': ['min', 'max', 'mean', 'std', 'sum'],
    'purchase_price': ['min', 'max', 'mean', 'std', 'sum']
})

print("\nAggregated statistics by manufacturer:")
print(aggregated_data)

# Plot pie chart for total purchase price by manufacturer
# plt.figure(figsize=(15, 4))
# data.groupby('manufacturer')['purchase_price'].sum().plot(kind='pie', autopct='%1.1f%%', startangle=90, legend=False)
# plt.title("The income in different manufacturers", fontsize=20)
# plt.show()

# Plot bar chart for money earned by manufacturer type
# plt.figure(figsize=(20, 4))
# earned_by_manufacturer = data.groupby('manufacturer')['purchase_price'].sum().sort_values(ascending=True).plot(kind='barh', color='g')
# plt.title("Money earned from vehicles by manufacturer type", fontsize=20)
# plt.xlabel("Purchase Price", fontsize=15)   
# plt.ylabel("Manufacturer", fontsize=15)
# plt.xticks(rotation=45)  # Rotate x-tick labels for better visibility
# plt.grid(color="green", linestyle="--", linewidth=0.5)
# plt.show()

# Scatter plot for selling price vs. purchase price
plt.figure(figsize=(12, 8))
sns.scatterplot(x='purchase_price', y='selling_price', data=data, hue='manufacturer', palette='viridis', alpha=0.6)
plt.title("Scatter Plot of Purchase Price vs. Selling Price by Manufacturer", fontsize=20)
plt.xlabel("Purchase Price", fontsize=15)
plt.ylabel("Selling Price", fontsize=15)
plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.show()



# setting the data on box plot 