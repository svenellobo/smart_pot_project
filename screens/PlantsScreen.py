from tkinter import ttk, Scrollbar, Canvas, StringVar, messagebox, font
import tkinter as tk
from utils.ComponentUtil import ComponentUtil as cu
from repository.PlantRepository import PlantRepository
from utils.FileUtil import FileUtil
from datasource.dto.PlantDto import PlantDto
from datasource.tk.PlantTk import PlantTk
from service.PlantDescriptionText import PlantDescriptionText
from screens.components.CustomEntry import CustomEntry




class PlantScreen(ttk.Frame):

    def __init__(self, parent, db):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=30, pady=30)
        self.db = db
        self.parent = parent
        self.repo = PlantRepository(self.db)
        self.visible = False
        self['relief'] = tk.RAISED
        self['borderwidth'] = 5
        self.main_screen()


    def main_screen(self):
        row = 0
        column = 1
        all_plants = self.repo.find_all_plants()


        y_scrollbar = tk.Scrollbar(self, orient="vertical")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar = tk.Scrollbar(self, orient="horizontal")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas = tk.Canvas(self, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, width=350, height=450)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        y_scrollbar.config(command=self.canvas.yview)
        x_scrollbar.config(command=self.canvas.xview)

        available_plants = tk.LabelFrame(self.canvas)

        self.canvas.create_window((0, 0), window=available_plants, anchor="nw")
        self.canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        available_plants.bind("<Configure>", self.canvas_scrolling)
        available_plants.bind("<MouseWheel>", self.canvas_scrolling)
        self.canvas.bind("<MouseWheel>", self.canvas_scrolling)

        for plant in all_plants:

            plant_preview = ttk.LabelFrame(available_plants)
            cu.place_component(plant_preview, row, column)

            plant_name = ttk.Label(plant_preview, text=plant.name)
            cu.place_component(plant_name, 0, 0, tk.EW)
            plant_name.bind("<Button-1>", lambda event, selected_plant=plant: self.selected_plant_data(selected_plant))

            plant_image = FileUtil.work_on_img(plant.plant_image, 50, 50)
            plant_preview_img = tk.Label(plant_preview, image=plant_image)
            plant_preview_img.image = plant_image
            cu.place_component(plant_preview_img, 0, 1)
            plant_preview_img.bind("<Button-1>", lambda event, selected_plant=plant: self.selected_plant_data(selected_plant))

            column += 1
            if column == 2:
                row += 1
                column = 0

        new_plant = ttk.LabelFrame(available_plants, text="Add new plant")
        cu.place_component(new_plant, 0, 0)

        lbl_new_pot_name = ttk.Label(new_plant, text="Enter pot name: ")
        cu.place_component(lbl_new_pot_name, 0, 0)

        add_plant_btn = ttk.Button(new_plant, text="Add Plant", command=self.add_new_plant_area)
        cu.place_component(add_plant_btn, 1, 0)

    def canvas_scrolling(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def selected_plant_data(self, selected_plant: PlantDto):

        plant_info_area = ttk.LabelFrame(self)
        cu.place_component(plant_info_area, 0, 4)

        self.close_btn = tk.Button(plant_info_area, bg="red", text="X", height=1, width=3, command=self.close)
        self.close_btn.grid(row=0, column=10, pady=5, padx=5, sticky=tk.NW)

        tabs = ttk.Notebook(plant_info_area)
        cu.place_component(tabs, 0, 0)

        main_plant_info = ttk.LabelFrame(tabs)
        cu.place_component(main_plant_info, 0, 0)

        lbl_plant_name = ttk.Label(main_plant_info, text=selected_plant.name, font=("Ariel", 12, "bold"))
        lbl_plant_name.grid(row=0, column=0, pady=5, padx=5, columnspan=2)

        plant_image = FileUtil.work_on_img(selected_plant.plant_image, 200, 200)
        lbl_plant_img = ttk.Label(main_plant_info, image=plant_image)
        lbl_plant_img.image = plant_image
        lbl_plant_img.grid(row=1, column=0, pady=5, padx=5, columnspan=2)


        lbl_ph = ttk.Label(main_plant_info, text="Ph Value:")
        cu.place_component(lbl_ph, 2, 0)
        lbl_ph_value = ttk.Label(main_plant_info, text=f"{selected_plant.plant_ph_low} - {selected_plant.plant_ph_high}")
        cu.place_component(lbl_ph_value, 2, 1)

        lbl_sunlight = ttk.Label(main_plant_info, text="Sunlight (h):")
        cu.place_component(lbl_sunlight, 3, 0)
        lbl_sunlight_value = ttk.Label(main_plant_info, text=f"{selected_plant.sunlight_low} - {selected_plant.sunlight_high}")
        cu.place_component(lbl_sunlight_value, 3, 1)

        lbl_temperature = ttk.Label(main_plant_info, text="Temperature (c°):")
        cu.place_component(lbl_temperature, 4, 0)
        lbl_temperature_value = ttk.Label(main_plant_info, text=f"{selected_plant.temperature_low} - {selected_plant.temperature_high}")
        cu.place_component(lbl_temperature_value, 4, 1)

        lbl_last_watering_date = ttk.Label(main_plant_info, text="Watering frequency (days): ")
        cu.place_component(lbl_last_watering_date, 5, 0)
        lbl_last_watering_date_value = ttk.Label(main_plant_info, text=selected_plant.watering)
        cu.place_component(lbl_last_watering_date_value, 5, 1)


        #PLANT TEXT
        plant_text_area = ttk.LabelFrame(main_plant_info)
        plant_text_area.grid(row=1, column=2, pady=20, padx=20)
        plant_text_box = tk.Text(plant_text_area, wrap=tk.WORD, font="Arial 12", height=15, width=40)
        cu.place_component(plant_text_box, 0, 0, tk.NSEW)
        if selected_plant.plant_info != "" and selected_plant.plant_info is not None:
            web_info = PlantDescriptionText(selected_plant, plant_text_box)
            web_info.start()
            plant_text_box.tag_config('heading', font=('Arial', 16, 'bold'))
            web_info.close()

        #SCROLLBAR
        scrollbar = tk.Scrollbar(plant_text_area, orient=tk.VERTICAL, command=plant_text_box.yview)
        scrollbar.grid(row=0, column=1, pady=2, padx=2, sticky=tk.NS)
        plant_text_box.config(yscrollcommand=scrollbar.set)

        tabs.add(main_plant_info, text="Plant Info")




        #UPDATE PLANT
        edit_tab = ttk.LabelFrame(tabs)

        selected_plant.plant_tk.name.set(selected_plant.name)
        selected_plant.plant_tk.plant_image.set(selected_plant.plant_image)
        selected_plant.plant_tk.plant_ph_low.set(selected_plant.plant_ph_low)
        selected_plant.plant_tk.plant_ph_high.set(selected_plant.plant_ph_high)
        selected_plant.plant_tk.sunlight_low.set(selected_plant.sunlight_low)
        selected_plant.plant_tk.sunlight_high.set(selected_plant.sunlight_high)
        selected_plant.plant_tk.temperature_low.set(selected_plant.temperature_low)
        selected_plant.plant_tk.temperature_high.set(selected_plant.temperature_high)
        selected_plant.plant_tk.watering.set(selected_plant.watering)
        selected_plant.plant_tk.plant_info.set(selected_plant.plant_info)

        new_plant_name = CustomEntry(edit_tab, 0, 0, "Enter plant name: ", selected_plant.plant_tk.name)
        new_plant_img = CustomEntry(edit_tab, 1, 0, "Enter image url: ", selected_plant.plant_tk.plant_image)
        new_plant_ph_low = CustomEntry(edit_tab, 2, 0, "Enter lowest pH value: ", selected_plant.plant_tk.plant_ph_low)
        new_plant_ph_high = CustomEntry(edit_tab, 3, 0, "Enter highest pH value: ", selected_plant.plant_tk.plant_ph_high)
        new_plant_sun_low = CustomEntry(edit_tab, 4, 0, "Enter min sunlight hours: ", selected_plant.plant_tk.sunlight_low)
        new_plant_sun_high = CustomEntry(edit_tab, 5, 0, "Enter max sunlight hours: ", selected_plant.plant_tk.sunlight_high)
        new_plant_temp_low = CustomEntry(edit_tab, 6, 0, "Enter min temperature: ", selected_plant.plant_tk.temperature_low)
        new_plant_temp_high = CustomEntry(edit_tab, 7, 0, "Enter max temperature: ", selected_plant.plant_tk.temperature_high)
        new_plant_watering = CustomEntry(edit_tab, 8, 0, "Enter watering frequency(days): ", selected_plant.plant_tk.watering)
        new_plant_info = CustomEntry(edit_tab, 8, 0, "Enter url to info .txt file (optional): ", selected_plant.plant_tk.plant_info)

        update_plant_lbl = ttk.Label(edit_tab, text=f"Update '{selected_plant.name}' plant?")
        update_plant_lbl.grid(row=9, column=0, padx=5, pady=5, sticky=tk.W)

        update_btn = tk.Button(edit_tab, text="Update", command=lambda: self.update_plant(selected_plant))
        update_btn.grid(row=9, column=1, padx=5, pady=5)

        # DELETE PLANT
        delete_plant_lbl = ttk.Label(edit_tab, text=f"Delete '{selected_plant.name}' plant?")
        delete_plant_lbl.grid(row=10, column=0, padx=5, pady=5, sticky=tk.W)

        delete_btn = tk.Button(edit_tab, text="Delete", bg="red", command=lambda: self.delete_plant(selected_plant))
        delete_btn.grid(row=10, column=1, padx=5, pady=5)

        tabs.add(edit_tab, text="Edit Plant")

    def close(self):
        self.destroy()
        self.parent.grid()



    def add_new_plant_area(self):
        self.grid(sticky=tk.NW)
        add_new_plant = ttk.LabelFrame(self)
        cu.place_component(add_new_plant, 0, 3)
        self.new_plant_tk = PlantTk()

        new_plant_name = CustomEntry(add_new_plant, 0, 0, "Enter plant name: ", self.new_plant_tk.name)
        new_plant_img = CustomEntry(add_new_plant, 1, 0, "Enter image url: ", self.new_plant_tk.plant_image)
        new_plant_ph_low = CustomEntry(add_new_plant, 2, 0, "Enter lowest pH value: ", self.new_plant_tk.plant_ph_low)
        new_plant_ph_high = CustomEntry(add_new_plant, 3, 0, "Enter highest pH value: ", self.new_plant_tk.plant_ph_high)
        new_plant_sun_low = CustomEntry(add_new_plant, 4, 0, "Enter min sunlight hours: ", self.new_plant_tk.sunlight_low)
        new_plant_sun_high = CustomEntry(add_new_plant, 5, 0, "Enter max sunlight hours: ", self.new_plant_tk.sunlight_high)
        new_plant_temp_low = CustomEntry(add_new_plant, 6, 0, "Enter min temperature: ", self.new_plant_tk.temperature_low)
        new_plant_temp_high = CustomEntry(add_new_plant, 7, 0, "Enter max temperature: ", self.new_plant_tk.temperature_high)
        new_plant_watering = CustomEntry(add_new_plant, 8, 0, "Enter watering frequency(days): ", self.new_plant_tk.watering)
        new_plant_info = CustomEntry(add_new_plant, 8, 0, "Enter url to info .txt file (optional): ", self.new_plant_tk.plant_info)

        add_plant_btn = ttk.Button(add_new_plant, text="Add Plant", command=self.add_plant)
        cu.place_component(add_plant_btn, 10, 0)


    def add_plant(self):
        name = self.new_plant_tk.name.get()
        img = self.new_plant_tk.plant_image.get()
        ph_low = self.new_plant_tk.plant_ph_low.get()
        ph_high = self.new_plant_tk.plant_ph_high.get()
        sun_low = self.new_plant_tk.sunlight_low.get()
        sun_high = self.new_plant_tk.sunlight_high.get()
        temp_low = self.new_plant_tk.temperature_low.get()
        temp_high = self.new_plant_tk.temperature_high.get()
        watering = self.new_plant_tk.watering.get()
        plant_info = self.new_plant_tk.plant_info.get()
        plant_web = None

        self.repo.add_plant(name, img, ph_low, ph_high, sun_low, sun_high, temp_low, temp_high,watering,plant_info, plant_web)
        self.destroy()
        PlantScreen(self.parent, self.db)

    def delete_plant(self, selected_plant):
        msg_box = tk.messagebox.askquestion('Delete Plant', f"Are you sure you want to delete '{selected_plant.name}' plant?",
                                            icon='warning')
        if msg_box == 'yes':
            self.repo.delete_plant(selected_plant)
            self.destroy()
            PlantScreen(self.parent, self.db)

    def update_plant(self, selected_plant):
        selected_plant.name = selected_plant.plant_tk.name.get()
        selected_plant.plant_image = selected_plant.plant_tk.plant_image.get()
        selected_plant.plant_ph_low = selected_plant.plant_tk.plant_ph_low.get()
        selected_plant.plant_ph_high = selected_plant.plant_tk.plant_ph_high.get()
        selected_plant.sunlight_low = selected_plant.plant_tk.sunlight_low.get()
        selected_plant.sunlight_high = selected_plant.plant_tk.sunlight_high.get()
        selected_plant.temperature_low = selected_plant.plant_tk.temperature_low.get()
        selected_plant.temperature_high = selected_plant.plant_tk.temperature_high.get()
        selected_plant.watering = selected_plant.plant_tk.watering.get()
        selected_plant.plant_info = selected_plant.plant_tk.plant_info.get()
        self.repo.update_plant(selected_plant)
        self.destroy()
        PlantScreen(self.parent, self.db)



