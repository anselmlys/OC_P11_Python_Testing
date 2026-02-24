from datetime import datetime


def is_future_competition(competition_date: str):
    competition_datetime = datetime.strptime(competition_date, '%Y-%m-%d %H:%M:%S')
    return competition_datetime >= datetime.now()
