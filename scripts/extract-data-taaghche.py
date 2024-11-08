#pip install requests
#pip install jdatetime
import requests
import json 
import jdatetime
import os 
from datetime import datetime


os.system('mkdir -p ./covers')

def fetch_books(list_type=1, list_value=135, offset="0-0-16-16", tracking_data=110160240, order=7):
    base_url = 'https://get.taaghche.com/v2/everything'
    filters = f'{{"list":[{{"type":{list_type},"value":{list_value}}},{{"type":50,"value":0}},{{"type":21,"value":0}},{{"type":3,"value":-106}},{{"value":0}}]}}'

    url = f"{base_url}?filters={filters}&offset={offset}&trackingData={tracking_data}&order={order}"

    response = requests.get(url)
    data = response.json()
    return data

def jalali_to_gregorian(jalali_date_str):
    if jalali_date_str:
        jalali_date = jdatetime.date(*map(int, jalali_date_str.split('/')))
        gregorian_date = jalali_date.togregorian()
        return gregorian_date
    else:
        return datetime.today()

def download_image(image_url, save_path):
    response = requests.get(image_url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

def convert_to_fixture(data, counter):
    download_image(data["coverUri"],f"covers/{counter}.jpg")
    fixture_data = {
        "model": "books.book",
        "pk": counter,
        "fields": {
            "title": data["title"],
            "description": data.get("shareText", ""),
            "published_date": jalali_to_gregorian(data.get('publishDate')).strftime("%Y-%m-%d"),
            "cover_image": f"covers/{counter}.jpg",
            "author": f"{data["authors"][0]['firstName']}{data["authors"][0]['lastName']}",
        }
    }
    return fixture_data


data = fetch_books()

fixture = []
for counter , book in enumerate(data['bookList']['books']):
    fixture_data = convert_to_fixture(book, counter+1)
    fixture.append(fixture_data)

with open("books.json", "w") as f:
    json.dump(fixture, f, indent=4, ensure_ascii=False)