import requests
from bs4 import BeautifulSoup
from tkinter import *


class Window:
    def __init__(self, links):
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Прогноз погоды")
        self.check = []
        self.label = Label(self.root, wraplength=800, font=("Trebuchet MS", 11))
        self.label.grid(row=0, column=0, columnspan=2)
        self.set_text(links)

        self.entry = Entry(self.root, width=50)
        self.entry.grid(row=1, column=0, sticky='E')

        self.btn = Button(self.root, text="Ввод", command=lambda x=links: self.check_input(links))
        self.btn.grid(row=1, column=1, sticky='W')

    def set_text(self, links):
        text = ""
        for city in links:
            self.check.append(city)
            text += city + ', '
        text = text[:-2]
        self.label.configure(text=text)

    def check_input(self, links):
        choice = self.entry.get()
        if choice not in self.check:
            return
        print(links[choice])
        Weather.parse_weather(self, links[choice])


class Weather:
    def __init__(self, link):
        self.link = link
        r = requests.get(self.link).text
        self.soup = BeautifulSoup(r, "html.parser")

    def get_cities(self):
        data = self.soup.find_all('a')
        links = {}
        for block in data:
            text = block.__str__()
            name = block.get_text()
            text = text[text.find('href="'):][6:]
            last = text.find('"')
            text = text[:last]
            if name not in ('Мобильная версия', 'Главная', 'О сайте', 'Частые вопросы (FAQ)', 'Контакты',
                            'Литва', 'Беларусь', 'Россия', 'Украина', 'Все страны', '>>>', 'См. на карте', '',
                            'Новости', 'Посмотреть', ' 21 сент. 2023'):
                links[name] = "https://rp5.ru" + text

        return links

    def parse_weather(self, link):
        w = Weather(link)
        data = w.soup.find('div', {'id': 'archiveString'})
        temp = data.find('span', {'class': 't_0'}).text
        text = data.find('a', {'class': 'ArchiveStrLink'})
        if text is None:
            text = data.find('div', {'class': 'ArchiveInfo'})
        text = text.text.replace("Архив погоды на метеостанции", "")
        self.label.configure(text=temp + "\n" + text)


w = Weather("https://rp5.ru/Погода_в_России")
d = w.get_cities()
window = Window(d)
window.root.mainloop()
print(d)
