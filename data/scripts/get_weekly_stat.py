from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import pandas as pd

# connect to yahoo api
oauth = OAuth2(None, None, from_file='./data/access_key.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()

handler = yfa.yhandler.YHandler(oauth)

settings = handler.sc.session.get('https://fantasysports.yahooapis.com/fantasy/v2/league/418.l.19600/settings', params={'format':'json'})

for week in range(1, 25):
    weekly_stats = handler.get_scoreboard_raw('418.l.19600', week=week)
    
    dict_stat_id = {}
    for stat in settings.json()['fantasy_content']['league'][1]['settings'][0]['stat_categories']['stats']:
        dict_stat_id[str(stat['stat']['stat_id'])] = stat['stat']['display_name']
    
    matchups = weekly_stats['fantasy_content']['league'][1]['scoreboard']["0"]['matchups']
    
    df_weekly_stats = pd.DataFrame(columns=['Team', 'FGM/A', 'FG%', 'FTM/A', 'FT%', '3PTM', 'PTS', 'OREB', 'REB', 'AST', 'ST', 'BLK', 'TO', 'A/T', 'GP'])
    
    for matchup in matchups.keys():
        if matchup != 'count':
            teams = matchups[matchup]['matchup']['0']['teams']
            for team in teams:
                if team != 'count':
                    team_stat = {}
                    team_stat['GP'] = teams[team]['team'][1]['team_remaining_games']['total']['completed_games']
                    team_stat['Team'] = teams[team]['team'][0][2]['name'].strip()
                    for stat in teams[team]['team'][1]['team_stats']['stats']:
                        team_stat[dict_stat_id[stat['stat']['stat_id']]] = stat['stat']['value']
                    df_weekly_stats = pd.concat([df_weekly_stats, pd.DataFrame.from_dict(team_stat, orient='index', columns=[0]).T])
    
    df_weekly_stats['Week'] = week
    df_weekly_stats = df_weekly_stats.reset_index(drop=True)
    df_weekly_stats.to_csv(f"./data/weekly_stats/week_{str(week).rjust(2, '0')}.csv", index=False)
    