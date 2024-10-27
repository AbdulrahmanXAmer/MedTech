import pandas as pd
import re

# Load the CSV file
df = pd.read_csv('medicine_data.csv')

# Function to extract salt names from the salt_composition column
def extract_salts(salt_comp):
    # Use regex to extract the salt names before the parentheses
    salts = re.findall(r'[A-Za-z\s]+(?=\s*\()', salt_comp)
    return salts

# Apply the function to extract salt names from the 'salt_composition' column
df['salt_names'] = df['salt_composition'].apply(extract_salts)

# Explode the 'salt_names' column to create one row per salt
df_exploded = df.explode('salt_names')

# Filter out any rows where the 'salt_names' is empty or just whitespace
df_exploded = df_exploded[df_exploded['salt_names'].str.strip() != '']

# Group by 'salt_names' and aggregate the 'side_effects' column by joining all effects for each salt
salt_side_effects = df_exploded.groupby('salt_names')['side_effects'].apply(lambda x: ', '.join(x)).reset_index()

# Function to clean and deduplicate side effects
def clean_side_effects(effects):
    # Split the string into individual effects, strip whitespace, deduplicate using a set, then join back
    unique_effects = set(effect.strip() for effect in effects.split(','))
    return ', '.join(unique_effects)

# Apply the cleaning function to the 'side_effects' column
salt_side_effects['side_effects'] = salt_side_effects['side_effects'].apply(clean_side_effects)

# Optionally, you can save the cleaned data to a new CSV file
salt_side_effects.to_csv('medicine_data_reduced.csv', index=False)
