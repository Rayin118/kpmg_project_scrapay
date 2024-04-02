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
    output_folder = 'Data_XBI_chinadata'
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, file_name + '.csv')
    df.to_csv(file_path, index=False)

# Define file names and corresponding id values
data_to_crawl = [
    ['中國鐵礦石價格指數', '61'],
    ['中國廢鋼價格指數', '78'],
    ['中國焦炭價格指數', '64'],
    ['中國鋼材價格指數', '65'],
    ['中國鋼胚價格指數', '79'],
    ['中國鋼鐵PMI', '69'],
    ['中國原材料庫存指數','123'],
    ['中國新訂單指數','120'],
    ['中國生產指數','119'],
    ['中國全國主要剛材品種庫存總量','117'],
    ['中國國內線材社會庫存量','68'],
    ['中國熱軋價格走勢','108'],
    ['中國冷軋價格走勢','109'],
    ['中國中板價格走勢','110'],
    ['鐵礦石主力合約收盤價格','180'],
    ['熱軋板卷主力合約收盤價格','181'],
    ['焦煤主力合約收盤價格','182']
]

# Call the function to crawl and save data
for item in data_to_crawl:
    crawl_and_save_data(item[0], item[1])
