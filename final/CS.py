import os
import requests
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

def crawl_product_data(product_name, value_code):
    # k parameter required
    def getTime():
        return int(round(time.time() * 1000))

    url = "https://data.stats.gov.cn/easyquery.htm?"
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    key = {}
    key['m'] = 'QueryData'
    key['dbcode'] = 'hgyd'
    key['rowcode'] = 'zb'
    key['colcode'] = 'sj'
    key['wds'] = '[]'
    key['dfwds'] = '[{"wdcode":"zb","valuecode":"' + value_code + '"},{"wdcode":"sj","valuecode":"last240"}]'
    key['k1'] = str(getTime())
    key['h'] = '1'

    r = requests.get(url, headers=header, params=key, verify=False)
    js = json.loads(r.text)

    length = len(js['returndata']['datanodes'])

    def getlist(l):
        lst = []
        for i in range(length):
            strdata = js['returndata']['datanodes'][i]['data']['strdata']
            lst.append(strdata)
        return lst

    lst = getlist(length)
    array = np.array(lst).reshape(4, 240)  # Reshape directly to (240, 4)
    df = pd.DataFrame(array)

    # Generate date range
    current_date = datetime.now()
    start_date = current_date.replace(day=1) - timedelta(days=1)
    start_date = start_date.replace(day=1)
    end_date = start_date.replace(year=start_date.year - 20, month=start_date.month + 1)
    delta = timedelta(days=1)
    date_range = []

    # Format dates as strings and add to the set
    while start_date >= end_date:
        date_range.append(start_date.strftime('%Y/%m'))
        start_date -= delta

    # Convert the set to a list
    date_range = list(set(date_range))

    # Sort the dates
    date_range.sort(reverse=True)


    df.columns = date_range
    df.index = [    ' CV(10K tons) ', 
                    ' ACCV(10K tons)', 
                    ' YOY(%)', 
                    ' ACCG(%)']

    # Swap rows and columns, and reset index to make date as a column
    df = df.transpose().reset_index()

    # Rename columns
    df.columns = [  'Date',
                    'CV(10K tons)', 
                    'ACCV(10K tons)', 
                    'YOY(%)', 
                    'ACCG(%)']
                  
    # Save the DataFrame to a CSV file in 'Data_cs_unclean' directory
    os.makedirs('Data_cs_unclean', exist_ok=True)
    file_name = os.path.join('Data_cs_unclean', 'data_' + product_name.replace(' ', '_') + '.csv')
    df.to_csv(file_name, index=False)

    return df


# Call the function to fetch data for different products and save as CSV files,value_code為該品項的網頁代號
products = [
    {"name": "鐵礦石", "value_code": "A020901"},
    {"name": "生鐵", "value_code": "A020913"},
    {"name": "粗鋼", "value_code": "A020914"},
    {"name": "鋼材", "value_code": "A020915"},
    {"name": "鋼筋", "value_code": "A020916"},
    {"name": "線材", "value_code": "A020917"},
    {"name": "冷軋薄版", "value_code": "A020918"},
    {"name": "中厚寬鋼帶", "value_code": "A020919"},
    {"name": "焦煤", "value_code": "A03010F"}
]

for product in products:
    crawl_product_data(product["name"], product["value_code"])
