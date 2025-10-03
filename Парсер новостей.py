from bs4 import BeautifulSoup
import requests
from time import sleep
from xl_create import writer
from datetime import datetime
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_img(url,folder):
    response = requests.get(url, stream=True, timeout=30)
    if response.status_code != 200:
        print(f"Ошибка загрузки: {response.status_code}")
        return
    r = open(rf'{folder}\{url.split("/")[-1]}', "wb")
    for value in response.iter_content(1024*1024):
        r.write(value)
    r.close()

def create_csv(all_news):
    with open(f"all_news_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv", "w", newline="", encoding="utf-8") as f:
        writer_csv = csv.writer(f)
        writer_csv.writerows(all_news)

def get_urls(page_count):
    print("Извиняюсь, но нужно подождать..")
    for page in range(1,page_count):
        url = f"https://habr.com/ru/news/page{page}/"


        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("article")

        for new in data:
            new_url = "https://habr.com" + new.find("a", class_="tm-title__link").get("href")
            yield new_url



def get_news():
    all_news = []
    text_final = ""
    folder = ""
    image_url = None
    while True:
        try:
            page_count = int(input("""Сколько страниц новостей вывести?
Ввод цифрой: """).strip()) + 1
            break

        except:
            print("Нужно ввести количество страниц числом")
    while True:
        m = input("""
Вы хотите скачать обложки новостей?
ДА - нажмите 1
Нет - нажмите 2
Ввод: """)
        if m == "1":
            folder = input(fr"""Скопируйте путь до папки.
Например C:\Users\User\Изображения
Ваш путь: """)
            break
        if m == "2":
            break
        else:
            print("Неизвестная комманда")

    for news in get_urls(page_count):
        response = requests.get(news, headers=headers)
        sleep(2)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("article")
        title = data.find("h1", class_="tm-title tm-title_h1").text
        create_time = data.find("time").get("title")

        if data.find("figure",class_="full-width" ) is not None:
            image_url =  data.find("figure",class_="full-width" ).find("img").get("src")
            if m == "1":
                try:
                    download_img(image_url,folder)
                except:
                    print("Ошибка пути. Фото скачаны не будут")
        text_block = data.find_all("p")

        for text in text_block:
            text_final += text.text + "\n"
        all_news.append([title,create_time, text_final, image_url])
        text_final = ""

    print(f"Собрано новостей: {len(all_news)}")
    return all_news



news_list = get_news()



while True:
    a = input("""
Нажмите 1 чтобы вывести новости в консоль.
Нажмите 2 чтобы загрузить новости в XL файл.
Нажмите 3 чтобы загрузить новости в CSV файл.
Нажмите 4 чтобы выполнить все функции и выйти.
Нажмите q/й чтобы выйти.

Ввод пользователя: """).strip()
    if a == "1":
        for news in news_list:
            print(f"""
            
Заголовок:{news[0]}
{news[1]}

{news[2]}""")


    elif a == "2":
        writer(news_list)


    elif a == "4":
        for news in news_list:
            print(f"""

Заголовок: {news[0]}
{news[1]}

{news[2]}""")
        writer(news_list)
        create_csv(news_list)
        print("Досвидания")
        break

    elif a.lower() == "q" or a.lower() == "й":
            print("Досвидания")
            break
    elif a == "3":
        create_csv(news_list)

    else:
        print("Неизвестная команда")