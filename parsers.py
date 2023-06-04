import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import os

url = 'https://www.gismeteo.ru/weather-cherkessk-5224/' # Ссылка на сайте гисметео на сегодня
url2 = 'https://www.gismeteo.ru/weather-cherkessk-5224/2-weeks/' # Ссылка на сайте гисметео на неделю
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
}


# Функция для вывода погоды на данный момент.
def current_weather(url, headers):
    req = requests.get(url, headers=headers)
    src = req.text

    with open("forecast.html", "w") as file:
        file.write(src)

    with open("forecast.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    sign = soup.find(
        "section", class_="content wrap"
    ).find(
        "div", class_="content-column column1"
    ).find(
        "section", class_="section section-content section-bottom-collapse"
    ).find(
        "div"
    ).find("a").find("div").find("div").find(class_="weather").find("div").find("span").find_next().text
    temperature = soup.find(
        "section", class_="content wrap"
    ).find("div", class_="content-column column1").find(
        "section", class_="section section-content section-bottom-collapse").find("div").find("a").find("div").find(
        "div").find(class_="weather").find("div").find("span").find_next().next_element.next_element.text

    return f"Сейчас в (Ваш Город) {sign}{temperature}🌡️"


# Функция для вывода прогноза на неделю.
def week_weather(url2, headers):
    req2 = requests.get(url2, headers=headers)
    src2 = req2.text

    with open("forecast_week.html", "w") as file:
        file.write(src2)

    with open("forecast_week.html") as file:
        src2 = file.read()

    soup2 = BeautifulSoup(src2, "lxml")
    week_days = soup2.find("section", class_="content wrap").find(
        class_="content-column column1").next_element.find_next_sibling().find_next().find_next().find_next().find_next().find_all("a")
    week = []

    ans = []
    ans2 = []

    for item in week_days:
        item = item.text
        week.append(item[:2] + ' ' + item[2:4].rstrip())

    week_temp = soup2.find("section", class_="content wrap").find(
        class_="content-column column1").next_element.find_next_sibling().find_next().find_next().find_next().find_next().find_next_sibling().find_next_sibling().find_next().find_next_sibling().find_next().find_next_sibling().find_all(
        "div",
        class_="value style_size_m")

    week_temperature = []

    for j in week_temp:
        j = j.text
        j = j[0:-2]
        if len(j) == 7:
            week_temperature.append(j[:2] + ' ' + j[5:7])
        else:
            week_temperature.append(j[:3] + ' ' + j[5:8])

    day = []
    day2 = []
    night = []
    night2 = []

    for i in week_temperature:
        day.append(i.split()[0])
        night.append(i.split()[1])

    day = day[:7]
    night = night[:7]
    week = week[:7]

    for i in day:
        i = i[1:]
        i = int(i)
        day2.append(i)

    for i in night:
        i = i[1:]
        i = int(i)
        night2.append(i)

    width = 0.4
    x_list = list(range(0, 7))
    y1_list = day2
    y2_list = night2
    x_indexes = np.arange(len(x_list))


    plt.title('График гистограммы на неделю.')
    plt.xticks(x_indexes, week)
    plt.xlabel('Дни')
    plt.ylabel('Температура')
    plt.bar(x_indexes - (width / 2), y2_list, label='Ночная температура', width=width)
    plt.bar(x_indexes + (width / 2), y1_list, label='Дневная температура', width=width)
    plt.savefig('image.png')

    for i in range(len(week)):
        ans.append(
            f"{week[i]}: ☀Днём: {week_temperature[i][:week_temperature[i].find(' ')]}  🌌Ночью:{week_temperature[i][week_temperature[i].rfind(' '):]}")

    for k in ans:
        if len(k.split(':')[0]) == 4:
            ans2.append(
                k.split(':')[0].ljust(5, ' ') + ' :' + '  ' + k.split()[2] + ' ' + k.split()[3] + ' ' + k.split()[
                    4] + ' ' + k.split()[5] + '\n')
        else:
            ans2.append(
                k.split(':')[0].ljust(5, ' ') + ':' + '  ' + k.split()[2] + ' ' + k.split()[3] + ' ' + k.split()[
                    4] + ' ' + k.split()[5] + '\n')

    return ans2
