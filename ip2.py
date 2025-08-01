import json
import random
import time
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://health-diet.ru/table_calorie/?ysclid=md8pgaau4o223703613'

headers = {
    "Accept": "/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
}

# Fetch the webpage content
req = requests.get(url, headers=headers)
src = req.text

# Save the content to an HTML file
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)

# Read the content back from the file
with open('index.html', 'r', encoding='utf-8') as file:
    src = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(src, 'lxml')

# Find all product links
all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
all_categories_dict = {}
for item in all_products_hrefs:
    item_text = item.text.strip()  # Убираем лишние пробелы
    item_href = 'https://health-diet.ru' + item.get('href')

    all_categories_dict[item_text] = item_href

# Save the dictionary to a JSON file with utf-8 encoding
with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories_dict.json', encoding='utf-8') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():
    if count == 0:
        rep = [",", ",", "-", "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html", "w", encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", "r", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not None:
        continue

    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f"data/{count}_{category_name}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    products_data = soup.find(class_='mzr-tc-group-table').find("tbody").find_all("tr")

    product_info = []

    for item in products_data:
        products_tds = item.find_all("td")

        title = products_tds[0].find('a').text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f"data/{count}_{category_name}.csv", "a", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    calories,
                    title,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json", "a", encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)



    count += 1
    print(f"# Итерация {count}, {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа закончена")
        break
    print(f"Осталось итераций: {iteration_count}")
    time.sleep(random.randrange(2, 4))






