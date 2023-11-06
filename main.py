from data.scripts.load_data import YfaDataLoad
from data.scripts.transform import transform_data, create_weekly_summary

if __name__ == '__main__':
    for league in [6315, 33128]:
        yfa_data = YfaDataLoad(league_id=league)
        yfa_data.download_weekly_data()
        transform_data(league_id=league)
        create_weekly_summary(league_id=league)