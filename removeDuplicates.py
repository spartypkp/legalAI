import pandas as pd

# Load your data
data = pd.read_csv("ca_node_eav_rows.csv")
print("Original: ",len(data))
data = pd.read_csv("duplicates.csv")
print("Duplicates: ",len(data))
data = pd.read_csv('cleaned_data.csv')
print("Cleaned: ",len(data))
# Identify duplicates based on all columns
print(len(data))
