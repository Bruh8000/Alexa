import requests
from bs4 import BeautifulSoup

# 1. Отправляем запрос к сайту
url = "http://books.toscrape.com/"
response = requests.get(url)

# 2. Проверяем, что запрос успешен (код 200)
if response.status_code == 200:
    print("Страница загружена!")
else:
    print("Ошибка:", response.status_code)

# 3. Создаём "суп" для парсинга
soup = BeautifulSoup(response.text, "html.parser")
print(soup.title.text)  # Выводим заголовок страницы

books = soup.find_all("article", class_="product_pod")

for book in books:
    # 1. Название книги
    title = book.h3.a["title"]

    # 2. Цена (убираем символ £)
    price = book.find("p", class_="price_color").text.replace("£", "")

    # 3. Рейтинг (из класса star-rating Four → 4)
    rating_class = book.find("p", class_="star-rating")["class"][1]
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_map.get(rating_class, 0)

    print(f"Книга: {title}, Цена: {price}, Рейтинг: {rating}")

##print(f"{item.text} : {item_href}")

