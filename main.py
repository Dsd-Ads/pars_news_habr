import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Здесь вам нужно указать информацию о базе данных (название и путь)
DATABASE_NAME = 'id.db'

def get_data_from_page(page_number):
    url = f'https://habr.com/ru/news/page{page_number}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find('div', class_='tm-articles-list')

    # Находим все элементы с тегом 'article' и атрибутом 'id' в указанном классе
    id_elements = data.find_all('article', {'id': True})

    # Сохраняем данные в базу данных
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    for element in id_elements:
        article_id = element['id']
        article_link = f'https://habr.com/ru/news/{article_id}/'

        # Проверяем, существует ли уже новость с таким article_id в базе данных
        cursor.execute("SELECT * FROM id WHERE id=?", (article_id,))
        existing_data = cursor.fetchone()
        if not existing_data:
            # Если новости с таким article_id еще нет в базе данных, добавляем ее в начало
            cursor.execute("INSERT INTO id (id, id_link) VALUES (?, ?)", (article_id, article_link))
            print(f"Новость с id={article_id} добавлена.")
        else:
            # Если новость с таким article_id уже есть, не добавляем ее
            print(f"Новость с id={article_id} уже есть в базе данных, не добавляем ее.")

    conn.commit()
    conn.close()

# Зададим количество страниц, которые хотим обработать
num_pages = 5

for page_number in range(1, num_pages + 1):
    print(f'Обработка страницы {page_number}...')
    get_data_from_page(page_number)
    # Добавим небольшую задержку, чтобы не нагружать сервер и не вызывать блокировку
    time.sleep(2)
