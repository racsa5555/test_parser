import requests
from bs4 import BeautifulSoup as BS
import lxml
from selenium import webdriver
import matplotlib.pyplot as plt

URL = 'https://www.finam.ru/'
APIKEY = "S4MR5WE3WND9R898"

class API:
    URL = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&"
    def __init__(self,api_key:str):
        self.api_key = api_key

    def get_top_gainers(self):
        url = self.URL + f"apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        gainers = data.get('top_gainers')[:10]
        result = {(item['ticker'], item['change_percentage']) for item in gainers}
        return result


    def get_top_losers(self):
        url = self.URL + f"apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        losers = data.get('top_losers')[:10]
        result = {(item['ticker'], item['change_percentage']) for item in losers}
        return result
    

def get_data_pars():
    driver = webdriver.Chrome()

    driver.get(URL)

    html_content = driver.page_source

    driver.quit()

    soup = BS(html_content, 'html.parser')
    soup2 = soup.find(class_ = 'Item__container--2AY undefined')
    tbody = soup2.find('tbody')
    rows = tbody.find_all('tr')
    unique = set()
    for row in rows:
        cells = row.find_all(name = 'td')
        for cell in cells:
            table = cell.find_all(name  = 'td')
            if table:
                for x in range(0,len(table) -1,3):
                    name = table[x].text
                    percent = table[x+2].text
                    unique.add((name,percent))
    return unique

def get_data_to_plt(data):
    data_dict = {}
    for item in data:
        company, change = item
        data_dict[company] = float(change[:-1].replace(',', '.'))

    sorted_data = sorted(data_dict.items(), key=lambda x: x[1])
    companies = [item[0] for item in sorted_data]
    changes = [item[1] for item in sorted_data]
    return companies,changes

def get_data_api():
    obj = API(APIKEY)
    t1 = obj.get_top_losers()
    t2 = obj.get_top_gainers()
    res = (*t1,*t2)
    return res


def main():
    data_html = get_data_pars()
    api_data = get_data_api()
    data = (*api_data,*data_html)
    companies,changes = get_data_to_plt(data)
    plt.figure(figsize=(12, 8))
    plt.barh(companies, changes, color='skyblue')
    plt.xlabel('Динамика котировок, %')
    plt.title('Динамика котировок компаний')
    plt.grid(axis='x')
    plt.savefig('stock_changes.png')

main()
