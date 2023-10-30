import pandas as pd
import os


def transform_data(league_id) -> None:
    print(f'---- transforming data to json for {league_id} ----')
    # Loop through each file in the directory
    file_dir = f'./data/league_{league_id}/weekly_stats'
    combined_df = pd.concat(
        [
            pd.read_csv(os.path.join(file_dir, file), encoding='utf-8') for file in
            os.listdir(file_dir)
        ],
        ignore_index=True
    )

    combined_df['Week'] = combined_df['Week'].astype(str)

    js_string = f"var weekly_stats = {combined_df.to_dict('records')}"

    with open(f'./static/js/data_{league_id}.js', 'w', encoding='utf-8') as f:
        f.write(js_string)
