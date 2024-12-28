from threading import Thread
import tkinter as tk
from datasource.dto.PlantDto import PlantDto
import requests
from bs4 import BeautifulSoup


class PlantDescriptionText(Thread):

    def __init__(self, plant: PlantDto, text_box):
        super().__init__()
        self.interrupted = False
        self.plant = plant
        self.text_box = text_box


    def run(self):
        while not self.interrupted:
            try:
                response = requests.get(self.plant.plant_web)
                web_parser = BeautifulSoup(response.text, 'html.parser')

                div = web_parser.find('div', class_="entry-content")
                remove = "text-align: right;"
                elements = div.find_all(['p', 'h2', 'h3'])

                for element in elements:

                    if element.name == 'h2' or element.name == 'h3':
                        self.text_box.insert(tk.END, element.text + '\n\n', 'heading')
                    else:
                        if element.get('style') == remove:
                            element.extract()
                        else:
                            self.text_box.insert(tk.END, element.text + '\n\n')


                self.text_box.config(state=tk.DISABLED)

            except:
                plant_txt = open(self.plant.plant_info, "r", encoding="utf8")
                self.text_box.insert(tk.END, plant_txt.read())
                self.text_box.config(state=tk.DISABLED)






    def close(self):
        self.interrupted = True


