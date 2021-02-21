import requests
from bs4 import BeautifulSoup
from ScrapperUtils import (normalize_date, get_first_day, genrate_daily_series, 
                            update_date_series, unpack, write_to_csv)

def get_daily_data():
    url = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"

    t = requests.get(url).text
    soup = BeautifulSoup(t, 'html.parser')

    table = soup.find('table', summary='Henry Hub Natural Gas Spot Price (Dollars per Million Btu)')

    rows = table.findAll('tr')[1:]

    csv_data = {'Date':[], 'price':[]}

    for row in rows:
        prices = row.findAll('td', class_='B3')
        prices = [price.get_text(strip=True) for price in prices ]
        
        try:
            date_str = row.find('td', class_='B6').get_text(strip=True)
            date_str = normalize_date(date_str)
            start_date = get_first_day(date_str)
            day_dict = genrate_daily_series(start_date)
            data = update_date_series(day_dict, prices)
            unpack(csv_data, data)
        except:
            continue
    
    return csv_data


if __name__=="__main__":
    print("starting now...")
    data = get_daily_data()
    write_to_csv(data, "Tabular_data/Data/daily.csv")
    print("Data Scrapped Successfully...")