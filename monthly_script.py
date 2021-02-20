import requests
from bs4 import BeautifulSoup
import pandas as pd
from My_Utils import normalize_date, generate_monthly_series, update_date_series, unpack


def get_monthly_data():
    url = "https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm"

    t2 = requests.get(url).text
    soup2 = BeautifulSoup(t2, 'html.parser')

    table = soup2.find('table', summary='Henry Hub Natural Gas Spot Price (Dollars per Million Btu)')

    rows = table.findAll('tr')[1:]

    csv_data = {'Date':[], 'price':[]}

    for row in rows:
        year = row.find("td", class_="B4")
        if year:
            year = year.get_text(strip=True)
            prices = row.findAll("td", class_="B3")
            prices = [price.get_text(strip=True) for price in prices]
            monthly = generate_monthly_series(year)
            data = update_date_series(monthly, prices)
            unpack(csv_data, data)
        else:
            pass
    
    df = pd.DataFrame(csv_data)

    return df

if __name__=="__main__":
    print("starting now...")
    df = get_monthly_data()
    print(df)