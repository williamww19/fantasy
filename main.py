from data.scripts.load_data import YfaDataLoad
from data.scripts.transform import transform_data

if __name__ == '__main__':
    yfa_data = YfaDataLoad(league_id=33128)
    yfa_data.download_weekly_data()
    transform_data()