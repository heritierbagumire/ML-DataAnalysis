import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Fetch data from users API
peoples_api = requests.get('http://127.0.0.1:3000/users')
peoples_api.raise_for_status()
peoples_api_data = peoples_api.json()

# Fetch data from educational API
peoples_educational_api = requests.get('http://127.0.0.1:3000/educational')
peoples_educational_api.raise_for_status()
peoples_educational_api_data = peoples_educational_api.json()

# Load data into DataFrames
vdf = pd.DataFrame(peoples_api_data)
odf = pd.DataFrame(peoples_educational_api_data)

# Merge the two datasets on the 'id' column
inner_merged_df = pd.merge(vdf, odf, on="id", how="outer")
print("the joined dataframes:", inner_merged_df)

# 1. Return 500,000 rows of data from your dataset
num_rows_to_return = 500000
if len(inner_merged_df) >= num_rows_to_return:
    dataset_sample = inner_merged_df.sample(n=num_rows_to_return, random_state=42)
else:
    dataset_sample = inner_merged_df

# 2. Describe your dataset
dataset_description = dataset_sample.describe(include='all')
print(dataset_description)

# 3. Find and replace null values from your dataset
print(dataset_sample.isnull().sum())

# Replace null values with mode for categorical columns
for column in dataset_sample.select_dtypes(include=['object']).columns:
    dataset_sample[column] = dataset_sample[column].fillna(dataset_sample[column].mode()[0])

print(dataset_sample.isnull().sum())

# 4. Perform basic data preprocessing
# Check if there are numerical columns
numerical_columns = dataset_sample.select_dtypes(include=['float64', 'int64']).columns

if numerical_columns.size > 0:
    # Apply scaling only if there are numerical columns
    scaler = StandardScaler()
    dataset_sample[numerical_columns] = scaler.fit_transform(dataset_sample[numerical_columns])
else:
    print("No numerical columns to scale.")

# Label encoding for categorical columns
label_encoder = LabelEncoder()
categorical_columns = dataset_sample.select_dtypes(include=['object']).columns
for column in categorical_columns:
    dataset_sample[column] = label_encoder.fit_transform(dataset_sample[column])

# Remove duplicates
dataset_sample.drop_duplicates(inplace=True)

print("After preprocessing:")
print(dataset_sample.head())

# 5. Create some features in your dataset
# Assuming there are timestamp columns like "createdAt" and "updatedAt"
if 'createdAt' in dataset_sample.columns:
    dataset_sample['createdAt_year'] = pd.to_datetime(dataset_sample['createdAt']).dt.year
    dataset_sample['createdAt_month'] = pd.to_datetime(dataset_sample['createdAt']).dt.month
    dataset_sample['createdAt_day'] = pd.to_datetime(dataset_sample['createdAt']).dt.day

# Create a new feature combining "role" and "status" columns
if 'role' in dataset_sample.columns and 'status' in dataset_sample.columns:
    dataset_sample['role_status'] = dataset_sample['role'].astype(str) + "_" + dataset_sample['status'].astype(str)

# Feature based on the length of the "content" column
if 'content' in dataset_sample.columns:
    dataset_sample['content_length'] = dataset_sample['content'].apply(lambda x: len(str(x)))

print("New features added:")
print(dataset_sample.head())
