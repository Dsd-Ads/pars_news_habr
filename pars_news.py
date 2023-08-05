import aiohttp
import asyncio
from bs4 import BeautifulSoup
import sqlite3
from summa import summarizer

# Здесь вам нужно указать информацию о базе данных (название и путь)
DATABASE_NAME = 'id.db'
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'
CHAT_ID = 'CHAT_ID'

async def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data=data) as response:
            if response.status == 200:
                print("Сообщение отправлено успешно")
            else:
                print("Ошибка при отправке сообщения")

async def check_send_value(url):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT send FROM id WHERE id_link = ?", (url,))
        send_value = cursor.fetchone()[0]
        conn.close()
        return send_value
    except sqlite3.Error as e:
        print(f"Ошибка при проверке значения 'send': {e}")
        return None

async def fetch_and_send_requests(url):
    try:
        await asyncio.sleep(2)  # Добавляем тайм-слип перед запросом
        send_value = await check_send_value(url)
        if send_value == 'Y':
            print(f"Сообщение для {url} не отправлено, так как значение 'send' равно 'Y'")
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Проверяем наличие ошибок в ответе
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.find('h1', class_="tm-title tm-title_h1").text
                news = soup.find('div', xmlns="http://www.w3.org/1999/xhtml").text
                new = summarizer.summarize(news, words=50)
                print(title)
                print(new)
                print(f"Успешный запрос к {url}")
                
                # Отправляем сообщение в Telegram
                message = f"{title}\n\n{new}\n\n{url}"
                await asyncio.sleep(5)  # Добавляем тайм-слип перед отправкой сообщения
                await send_telegram_message(message)
                
                # Обновляем запись в базе данных, записывая значение "Y" в столбец 'send'
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                cursor.execute("UPDATE id SET send = ? WHERE id_link = ?", ('Y', url))
                conn.commit()
                conn.close()
                
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе к {url}: {e}")
        # Пропускаем текущую страницу и переходим к следующей
        return
    except Exception as e:
        print(f"Ошибка при обработке страницы {url}: {e}")

async def main():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        # Получаем все ссылки из столбца id_link
        cursor.execute("SELECT id_link FROM id")  # Замените 'table_name' на имя вашей таблицы
        rows = cursor.fetchall()

        tasks = [fetch_and_send_requests(url) for url, in rows]

        await asyncio.gather(*tasks)

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(main())
