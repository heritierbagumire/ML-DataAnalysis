# Summary of the dataset
print(data.info())

# Check for missing values
print(data.isnull().sum())

# Fill or drop missing values
data.fillna(0, inplace=True)  # Replace NaNs with 0
# OR
data.dropna(inplace=True)  # Drop rows with missing values

# Rename columns for better readability (optional)
data.rename(columns={"old_name": "new_name"}, inplace=True)

# Basic statistics
print(data.describe())


