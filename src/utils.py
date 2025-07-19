import datetime

# Convert a date string from 'YYYY-MM-DD' format to 'DD/MM/YYYY' format.
def norm_date(date: str) -> str:
    return f'{date[8:10]}/{date[5:7]}/{date[:4]}'
