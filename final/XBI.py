import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

def crawl_and_save_data(file_name, id_value):
    # Define header and parameters
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    key = {'id': id_value, 'type': '0'}
    url = "https://m.steelx2.com/database.aspx?"

    # Send request to the server
    response = requests.get(url, headers=header, params=key)

    # Parse HTML response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <tr> tags
    rows = soup.find_all('tr')

    # Initialize an empty list to store extracted data
    extracted_data = []

    # Iterate over each <tr> tag
    for row in rows:
       # Find all <td> tags in the row
       cols = row.find_all('td')

       # If the row contains <td> tags
       if cols:
           # Extract date and value
           date = cols[0].text.strip()
           value = cols[1].text.strip()

           # Find change and change percentage
           change_tag = cols[2].find('em') or cols[2].find('span')
           change_percentage_tag = cols[3].find('em') or cols[3].find('span')

           # If change and change percentage tags are found, extract them
           if change_tag and change_percentage_tag:
               change = change_tag.text.strip()
               change_percentage = change_percentage_tag.text.strip()

               # Append extracted data to the list
               extracted_data.append((date, value, change, change_percentage))

    # Convert to DataFrame
    df = pd.DataFrame(extracted_data, columns=['date', 'value', 'change', 'change percentage'])

    # Print DataFrame
    # print(df)

    # Save DataFrame to CSV file
    output_folder = 'Data_XBI_chinadata_unclean'
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name + '.csv')
    df.to_csv(file_path, index=False)

# Define file names and corresponding id values
data_to_crawl = [
    ['中國_鐵礦石價格指數_日', '61'],
    ['中國_廢鋼價格指數_日', '78'],
    ['中國_鋼材價格指數_日', '65'],
    ['中國_鋼胚價格指數_日', '79'],
    ['中國_鋼鐵PMI_週', '69'],
    ['中國_原材料庫存指數_月','123'],
    ['中國_新訂單指數_月','120'],
    ['中國_生產指數_月','119'],
    ['中國_全國主要剛材品種庫存總量_週','117'],
    ['中國_國內線材社會庫存量_週','68'],
    ['中國_熱軋價格走勢_日','108'],
    ['中國_冷軋價格走勢_日','109'],
    ['中國_中板價格走勢_日','110'],
    ['中國_鐵礦石主力合約收盤價格_日','180'],
    ['中國_熱軋板卷主力合約收盤價格_日','181'],
    ['中國_焦煤主力合約收盤價格_日','182']
]

# Call the function to crawl and save data
for item in data_to_crawl:
    crawl_and_save_data(item[0], item[1])
