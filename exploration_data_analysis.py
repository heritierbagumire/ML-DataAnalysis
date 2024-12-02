import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder  # Fixed typo

try:
    # Fetch data from users API
    peoples_api = requests.get('http://127.0.0.1:3000/users')
    peoples_api.raise_for_status()  # Raise an error if fetching fails
    peoples_api_data = peoples_api.json()  # Parse JSON response
    
    # Fetch data from educational API
    peoples_educational_api = requests.get('http://127.0.0.1:3000/educational')
    peoples_educational_api.raise_for_status()  # Raise an error if fetching fails
    peoples_educational_api_data = peoples_educational_api.json()  # Fixed variable
    
    # Load data into DataFrames
    vdf = pd.DataFrame(peoples_api_data)  # Ensure correct JSON key usage
    odf = pd.DataFrame(peoples_educational_api_data)  # Ensure correct JSON key usage
    
    inner_merged_df = pd.merge(vdf, odf, on="id", how="outer")
    print(inner_merged_df)

    
    # print("Users DataFrame:")
    # print(vdf)
    
    # print("\nEducational Content DataFrame:")
    # print(odf)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
