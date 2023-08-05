# pars_news_habr
Парсер новостей Habr.com
Этот проект представляет собой парсер новостей с популярного технического ресурса Habr.com с отправкой рассылки в Telegram.
Функциональность
Парсинг последних новостей с главной страницы Habr.com с помощью BeautifulSoup
Сохранение данных о новостях (id и ссылка) в SQLite базу данных
Асинхронный обход сохраненных ссылок на новости с помощью aiohttp
Формирование краткого описания новости с помощью библиотеки summa
Отправка уведомления в Telegram канал с помощью Telegram Bot API
Запуск
Установить зависимости pip install -r requirements.txt
Запустить сбор данных python main.py
Запустить рассылку python pars_news.py
Перед запуском необходимо указать свои данные для подключения к Telegram в файле pars_news.py.
Пример работы
После запуска скриптов в указанный Telegram канал будут отправляться уведомления о новых новостях примерно следующего вида:
Заголовок новости
Краткое описание новости из 2-3 предложений

Ссылка на новость
Таким образом реализуется простая автоматическая рассылка обзора последних новостей технического ресурса.
Лицензия
Данный проект распространяется под лицензией MIT.