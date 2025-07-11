import pandas as pd
from datetime import datetime, timedelta, date

def convert_to_datetime_column(df: pd.DataFrame, col: str, fmt: str = "%d/%m/%Y") -> pd.DataFrame:
    df[col] = pd.to_datetime(df[col], format=fmt)
    return df

def format_date_for_crossfit_url(date_obj: date) -> str:
    return date_obj.strftime('%y%m%d')

def get_week_dates(reference: date) -> list:
    monday = reference - timedelta(days=reference.weekday())
    return [monday + timedelta(days=i) for i in range(7)]

def english_to_french_weekday(day_name: str) -> str:
    mapping = {
        "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
        "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi",
        "Sunday": "Dimanche"
    }
    return mapping.get(day_name, "")
