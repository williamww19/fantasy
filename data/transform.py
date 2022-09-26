import pandas as pd

stats = pd.read_excel(
    './2021/BBM_PlayerRankings.xls', 
    usecols= ['Own', 'Round', 'Rank', 'Name', 'Team', 'Pos', 'USG', 
              #'g', 'm/g', 'p/g', '3/g', 'r/g', 'a/g', 's/g', 'b/g', 'fg%', 'fga/g', 'ft%', 'fta/g', 'or/g', 'to/g', 
              #'ato', 'pV', '3V', 'rV', 'aV', 'sV', 'bV', 'fg%V', 'ft%V', 'orV', 'toV', 'atoV'
              ]
    )

stats.to_json('./data/stats.json', orient='records')
