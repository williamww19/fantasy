import pandas as pd
import os

# Loop through each file in the directory
combined_df = pd.concat(
    [
        pd.read_excel(f'./data/weekly_stats/{file}') for file in os.listdir('./data/weekly_stats')
    ],
    ignore_index=True
)

combined_df['Week'] = combined_df['Week'].astype(str)

js_string = f"var weekly_stats = {combined_df.to_dict('records')}"

with open('./static/js/data.js', 'w') as f:
    f.write(js_string)