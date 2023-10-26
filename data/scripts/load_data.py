from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import pandas as pd


# connect to yahoo api
oauth = OAuth2(None, None, from_file='./secret/access_key.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()


class YfaDataLoad(object):
    def __init__(self, league_id):
        self.league_id = league_id
        self.handler = yfa.yhandler.YHandler(oauth)

    def get_game_key(self) -> int:
        response = self.handler.sc.session.get('https://fantasysports.yahooapis.com/fantasy/v2/game/nba',
                                          params={'format': 'json'})
        response_json = response.json()
        game_key = response_json['fantasy_content']['game'][0]['game_key']
        return game_key

    def get_settings(self, game_key, league_id):
        settings = self.handler.sc.session.get(
            f'https://fantasysports.yahooapis.com/fantasy/v2/league/{game_key}.l.{league_id}/settings',
            params={'format': 'json'})
        return settings

    def get_current_week(self, game_key, league_id) -> int:
        response = self.handler.sc.session.get(f'https://fantasysports.yahooapis.com/fantasy/v2/league/{game_key}.l.{league_id}', params={'format':'json'})
        response_json = response.json()
        current_week = response_json['fantasy_content']['league'][0]['current_week']
        return current_week

    def download_weekly_data(self) -> None:
        print('---- downloading data ----')
        game_key = self.get_game_key()
        settings = self.get_settings(game_key, self.league_id)
        current_week = self.get_current_week(game_key, self.league_id)

        for week in range(1, current_week+1):
            weekly_stats = self.handler.get_scoreboard_raw(f'{game_key}.l.{self.league_id}', week=week)

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
