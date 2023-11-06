import os

import pandas as pd


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


def create_weekly_summary(league_id):
    print(f'---- creating weekly summary for {league_id} ----')
    file_dir = f'./data/league_{league_id}/weekly_stats'
    for file in os.listdir(file_dir):
        df_week = pd.read_csv(os.path.join(file_dir, file), encoding='utf-8')
        week = df_week['Week'].unique()[0]
        df_week['TO'] = -df_week['TO']
        df_week_summary = pd.merge(df_week['Team'], df_week['Team'], how='cross')
        df_week_summary = df_week_summary[df_week_summary['Team_x'] != df_week_summary['Team_y']]
        df_week_summary['results'] = df_week_summary.apply(
            lambda row: compare_team_stats(df_week, row['Team_x'], row['Team_y']), axis=1)
        df_week_summary_pivot = df_week_summary.pivot(index='Team_x', columns='Team_y', values='results')
        df_week_summary_pivot.to_csv(f'./data/league_{league_id}/weekly_summary/{file}')


def compare_team_stats(df_week: pd.DataFrame, team_a: str, team_b: str) -> str:
    stats_col = ['FG%', 'FT%', '3PTM', 'PTS', 'OREB', 'REB', 'AST', 'ST', 'BLK', 'TO', 'A/T']
    stats_comp = df_week.loc[df_week['Team'].isin([team_a, team_b]), stats_col].T
    stats_comp.columns = ['Team_x', 'Team_y']
    win = ((stats_comp['Team_x'] - stats_comp['Team_y']) > 0).sum()
    tie = ((stats_comp['Team_x'] - stats_comp['Team_y']) == 0).sum()
    loss = ((stats_comp['Team_x'] - stats_comp['Team_y']) < 0).sum()

    return f'{win}-{loss}-{tie}'
