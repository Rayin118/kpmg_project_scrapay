import os
import requests
import csv
from datetime import datetime

def crawl_and_save_data(file_name, A):
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    key = {'A': A}
    url = "https://fubon-ebrokerdj.fbs.com.tw/Z/ZH/ZHG/CZHG.djbcd?"

    response = requests.get(url, headers=header, params=key)
    data = response.text 

    # 找到缺少逗号的位置插入逗號
    index_to_insert_comma = [i for i, char in enumerate(data) if char.isdigit() and data[i-1] == ' ']

    # 插入逗號
    for index in reversed(index_to_insert_comma):
        data = data[:index] + ',' + data[index:]

    data_list = data.split(',')
    date_list = data_list[:(len(data_list)//2)]  # 獲得日期列表
    value_list = data_list[len(data_list)//2:]  # 獲得對應值列表

    data_dict = dict(zip(date_list, value_list))

    # 儲存到資料夾中
    os.makedirs('Data_fubon_material_unclean', exist_ok=True)
    file_path = os.path.join('Data_fubon_material_unclean', file_name)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['日期', 'CV'])  
        for date, value in data_dict.items():
            writer.writerow([date, value])

# 文件與對應A值
data_files = [
    ('熱軋中鋼盤價_三個月.csv', '200070'),
    ('竹節鋼筋南5分以上_週.csv', '200600'),
    ('廢鋼豐興_週.csv', '201190'),
    ('鋼筋豐興廠交價_週.csv', '200960'),
    ('倫敦鎳三個月期貨價_週.csv', '200990'),
    ('倫敦鎳現貨價_週.csv', '200540'),
    ('鎳倫敦LME_庫存量_日.csv', '201400')
]


for file_name, A_value in data_files:
    crawl_and_save_data(file_name, A_value)
