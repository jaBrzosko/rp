import pandas as pd
import json

# Example DataFrame
data = {
    "name": ["John", "Jane", "Jake"],
    "age": [30, 25, 22],
    "city": ["New York", "Los Angeles", "Chicago"]
}

df = pd.DataFrame(data)
print(df)
# Specify the file name where you want to save the JSON data
file_name = 'data/dataframe.json'

# Convert DataFrame to JSON and save to file
df.to_json(file_name, orient='records', indent=4)

print(f"DataFrame has been saved to {file_name}")

file_name = 'data.json'
# Open the file in write mode and use json.dump() to write the Python object to the file
with open(file_name, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data has been saved to {file_name}")
