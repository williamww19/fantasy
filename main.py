from data.scripts.load_data import YfaDataLoad
from data.scripts.transform import transform_data_to_json, create_weekly_summary

if __name__ == '__main__':
    for league in [24138, 32858]:
        yfa_data = YfaDataLoad(league_id=league)
        yfa_data.download_weekly_data()
        transform_data_to_json(league_id=league)
        create_weekly_summary(league_id=league)