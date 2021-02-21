import datetime
from dateutil import parser
import csv


def normalize_date(date:str):
    date = date.replace("-", " ").replace("  ", " ")
    return date


def get_first_day(date:str):
    date_list = date.split(" ")
    year, month, day = date_list[0], date_list[1], date_list[2]
    return f'{year} {month} {day}'


def genrate_daily_series(date:str):
    dx = parser.parse(date)
    day_dict = {}
    day_dict[dx.strftime('%d/%m/%Y')] = 0
    for i in range(1, 5):
        day_dict.setdefault((dx + datetime.timedelta(days=i)).strftime('%d/%m/%Y'), 0)
    return day_dict


def generate_monthly_series(year:str):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_dict = {}

    for month in months:
        month_dict.setdefault(f'{year} {month}', 0)
    return month_dict


def update_date_series(series:dict, prices:list):
    idx = 0
    for k, _ in series.items():
        series[k] = prices[idx]
        idx+=1
    return series

def unpack(main:dict, temp:dict):
    for k, v in temp.items():
        main['Date'].append(k)
        main['price'].append(v)

def write_to_csv(data:dict, path:str):
    with open(path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))