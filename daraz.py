import json
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

search = input("Enter search Query: \n")
query = search.replace(" ", "+")

items = []
count = 0
temp = 1


def getdata(keyword, page):
    global items
    global count
    global temp
    url = 'https://www.daraz.com.np/catalog/?spm=a2a0e.searchlist.pagination.2.2f242696mDYuRp&_keyori=ss&from=input&q='+keyword+'&page='+str(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    target_script_tag = soup.find('script', string=lambda s: s and 'window.pageData' in s)
    if count == temp:
        return
    else:
        temp = items.__len__()
        if target_script_tag:
            script_content = target_script_tag.string

            json_data = script_content.split('=', 1)[1]

            data = json.loads(json_data)
            list_items = data.get("mods", {}).get("listItems", [])

            for item in list_items:
                data = {
                    'name': item.get("name"),
                    'list_price': item.get("priceShow"),
                    'old_price': item.get("originalPrice"),
                    'description': item.get("description", ["No description"]),
                    'image': item.get("image")
                }
                items.append(data)
                count = items.__len__()
            print(items)
            print(count)
            print(temp)

            csv_file_path = search + '.csv'
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['name', 'list_price', 'old_price', 'description', 'image']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write the header
                writer.writeheader()

                # Write the data
                writer.writerows(items)

            print(f'CSV file created: {csv_file_path}')
            page += 1
            getdata(keyword, page)

        else:
            print("Target script tag not found.")
            return


getdata(query, 1)
