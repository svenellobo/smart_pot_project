from tkinter import ttk, Scrollbar, StringVar, messagebox, IntVar
import tkinter as tk
from utils.ComponentUtil import ComponentUtil as cu
from datasource.dto.PotDto import PotDto
from repository.PotRepository import PotRepository
from utils.FileUtil import FileUtil
from screens.components.CustomScale import CustomScale
from repository.PlantRepository import PlantRepository
from datetime import datetime as dt
from screens.components.CustomEntry import CustomEntry
from repository.ValuesRepository import ValuesRepository
import matplotlib.pyplot as plt






class PotScreen(ttk.Frame):

    def __init__(self, parent, db):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=30, pady=30)
        self.db = db
        self.parent = parent
        self.repo = PotRepository(self.db)
        self.repo_plant = PlantRepository(self.db)
        self.repo_values = ValuesRepository(self.db)
        self.visible = False
        self['relief'] = tk.RAISED
        self['borderwidth'] = 5
        self.load_images()
        self.main_screen()




    def main_screen(self):
        row = 0
        column = 1
        all_pots = self.repo.find_all_pots()

        y_scrollbar = tk.Scrollbar(self, orient="vertical")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar = tk.Scrollbar(self, orient="horizontal")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas = tk.Canvas(self, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, width=350, height=450)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        y_scrollbar.config(command=self.canvas.yview)
        x_scrollbar.config(command=self.canvas.xview)

        available_pots = tk.LabelFrame(self.canvas)

        self.canvas.create_window((0, 0), window=available_pots, anchor="nw")
        self.canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        available_pots.bind("<Configure>", self.canvas_scrolling)
        available_pots.bind("<MouseWheel>", self.canvas_scrolling)
        self.canvas.bind("<MouseWheel>", self.canvas_scrolling)


        for pot in all_pots:
            pot.pot_tk.name.set(pot.name)

            self.pot_preview = ttk.LabelFrame(available_pots)
            cu.place_component(self.pot_preview, row, column)

            pot_name = ttk.Label(self.pot_preview, text=f"'{pot.name}' pot")
            cu.place_component(pot_name, 0, 0, tk.W)
            pot_name.bind("<Button-1>", lambda event, selected_pot=pot: self.selected_pot_data(selected_pot))



            self.pot_plant = ttk.Label(self.pot_preview, text="Empty")
            cu.place_component(self.pot_plant, 1, 1)


            if pot.plant_id is not None:
                selected_plant = self.repo_plant.fetch_plant_by_id(pot.plant_id)
                if selected_plant is not None:
                    self.pot_plant.config(text=selected_plant.name)
                    pot.plant = selected_plant

            pot_image = FileUtil.work_on_img(pot.pot_img, 50, 50)
            pot_preview_img = ttk.Label(self.pot_preview, image=pot_image)
            pot_preview_img.image = pot_image
            cu.place_component(pot_preview_img, 0, 1)
            pot_preview_img.bind("<Button-1>", lambda event, selected_pot=pot: self.selected_pot_data(selected_pot))

            # STATUS PREVIEW
            self.status_preview = ttk.Labelframe(self.pot_preview)
            cu.place_component(self.status_preview, 1, 0)

            self.pot_ph_status_preview = ttk.Label(self.status_preview, image=None)
            self.pot_ph_status_preview.grid(row=0, column=0, pady=0, padx=0)

            self.pot_sun_status_preview = ttk.Label(self.status_preview, image=None)
            self.pot_sun_status_preview.grid(row=0, column=1, pady=0, padx=0)

            self.pot_temperature_status_preview = ttk.Label(self.status_preview, image=None)
            self.pot_temperature_status_preview.grid(row=0, column=2, pady=0, padx=0)

            self.pot_watering_status_preview = ttk.Label(self.status_preview, image=None)
            self.pot_watering_status_preview.grid(row=0, column=3, pady=0, padx=0)


            if pot.plant is not None:
                self.set_status_imgs(pot)


            column += 1
            if column == 2:
                row += 1
                column = 0

        #ADD NEW POT
        new_pot = ttk.LabelFrame(available_pots, text="Add new pot")
        cu.place_component(new_pot, 0, 0)

        lbl_new_pot_name = ttk.Label(new_pot, text="Enter pot name: ")
        cu.place_component(lbl_new_pot_name, 0, 0)

        self.new_pot = StringVar()
        enter_new_pot_name = ttk.Entry(new_pot, textvariable=self.new_pot)
        cu.place_component(enter_new_pot_name, 1, 0)

        add_pot_btn = ttk.Button(new_pot, text="Add pot", command=self.make_pot)
        cu.place_component(add_pot_btn, 2, 0)


    def canvas_scrolling(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")


    def selected_pot_data(self, selected_pot: PotDto):

        self.pot_info_area = tk.LabelFrame(self)
        cu.place_component(self.pot_info_area, 0, 3)

        self.close_btn = tk.Button(self.pot_info_area, bg="red", text="X", height=1, width=3, command=self.close)
        self.close_btn.grid(row=0, column=10, pady=5, padx=5, sticky=tk.NW)

        name_display = ttk.Label(self.pot_info_area, )
        name_display.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        #POT INFO
        tabs = ttk.Notebook(self.pot_info_area)
        cu.place_component(tabs, 0, 0)



        self.selected_pot_area = ttk.LabelFrame(tabs)
        cu.place_component(self.selected_pot_area, 0, 0)

        if selected_pot.plant_id is not None:
            values = self.repo_values.fetch_all_values(selected_pot.id, selected_pot.plant_id)

            if values is not None:
                converted_time = dt.strptime(values.watering, "%Y-%m-%d %H:%M:%S.%f")
                new_time_value = converted_time.strftime("%m-%d-%Y")
                selected_pot.pot_tk.ph_value.set(values.ph_value)
                selected_pot.pot_tk.sunlight.set(values.sunlight_value)
                selected_pot.pot_tk.temperature.set(values.temperature_value)
                selected_pot.pot_tk.last_watering_date.set(new_time_value)


        self.lbl_pot_name = ttk.Label(self.selected_pot_area, text=f"'{selected_pot.pot_tk.name.get()}' pot", font=("Ariel", 12, "bold"))
        self.lbl_pot_name.grid(row=0, column=0, pady=5, padx=5, columnspan=2)

        if selected_pot.plant_id is not None:
            lbl_plant_name = ttk.Label(self.selected_pot_area, text=f"'{selected_pot.plant.name}' plant",
                                          font=("Ariel", 12, "bold"))
            lbl_plant_name.grid(row=0, column=2, pady=5, padx=5, columnspan=2)

        pot_image = FileUtil.work_on_img(selected_pot.pot_img, 150, 150)
        self.lbl_pot_img = ttk.Label(self.selected_pot_area, image=pot_image)
        self.lbl_pot_img.image = pot_image
        self.lbl_pot_img.grid(row=1, column=0, pady=5, padx=5, columnspan=4)

        last_pot_data = ttk.Labelframe(self.selected_pot_area)
        last_pot_data.grid(row=2, column=0, pady=5, padx=5, columnspan=2)

        lbl_heading = ttk.Label(last_pot_data, text="Last recorded data:", font=3)
        lbl_heading.grid(row=2, column=0, pady=5, padx=5, columnspan=2)



        self.lbl_ph = ttk.Label(last_pot_data, text="pH Value:")
        cu.place_component(self.lbl_ph, 3, 0, tk.W)
        self.lbl_ph_value = ttk.Label(last_pot_data, textvariable=selected_pot.pot_tk.ph_value)
        cu.place_component(self.lbl_ph_value, 3, 1)

        self.lbl_sunlight = ttk.Label(last_pot_data, text="Sunlight (h):")
        cu.place_component(self.lbl_sunlight, 4, 0, tk.W)
        self.lbl_sunlight_value = ttk.Label(last_pot_data, textvariable=selected_pot.pot_tk.sunlight)
        cu.place_component(self.lbl_sunlight_value, 4, 1)

        self.lbl_temperature = ttk.Label(last_pot_data, text="Temperature (C°):")
        cu.place_component(self.lbl_temperature, 5, 0, tk.W)
        self.lbl_temperature_value = ttk.Label(last_pot_data, textvariable=selected_pot.pot_tk.temperature)
        cu.place_component(self.lbl_temperature_value, 5, 1)

        self.lbl_last_watering_date = ttk.Label(last_pot_data, text="Last watering:")
        cu.place_component(self.lbl_last_watering_date, 6, 0, tk.W)

        self.lbl_last_watering_date_value = ttk.Label(last_pot_data, textvariable=selected_pot.pot_tk.last_watering_date)
        cu.place_component(self.lbl_last_watering_date_value, 6, 1)



        #PLANT VALUES
        if selected_pot.plant is not None:
            optimal_data = ttk.Labelframe(self.selected_pot_area)
            optimal_data.grid(row=2, column=2, pady=5, padx=5, columnspan=2)

            lbl_heading_optimal = ttk.Label(optimal_data, text="Optimal conditions:", font=3)
            lbl_heading_optimal.grid(row=2, column=2, pady=5, padx=5, columnspan=2)

            lbl_plant_ph = ttk.Label(optimal_data, text="Optimal pH:")
            cu.place_component(lbl_plant_ph, 3, 2, tk.W)
            lbl_plant_ph_value = ttk.Label(optimal_data, text=f"{selected_pot.plant.plant_ph_low}-{selected_pot.plant.plant_ph_high}")
            cu.place_component(lbl_plant_ph_value, 3, 3)

            lbl_plant_sun = ttk.Label(optimal_data, text="Optimal sunlight(h):")
            cu.place_component(lbl_plant_sun, 4, 2, tk.W)
            lbl_plant_sun_value = ttk.Label(optimal_data, text=f"{selected_pot.plant.sunlight_low}-{selected_pot.plant.sunlight_high}")
            cu.place_component(lbl_plant_sun_value, 4, 3)

            lbl_plant_temperature = ttk.Label(optimal_data, text="Optimal temperature (C°):")
            cu.place_component(lbl_plant_temperature, 5, 2, tk.W)
            lbl_plant_temperature_value = ttk.Label(optimal_data, text=f"{selected_pot.plant.temperature_low}-{selected_pot.plant.temperature_high}")
            cu.place_component(lbl_plant_temperature_value, 5, 3)

            lbl_plant_watering = ttk.Label(optimal_data, text="Watering frequency(days):")
            cu.place_component(lbl_plant_watering, 6, 2, tk.W)
            lbl_plant_watering_value = ttk.Label(optimal_data, text=selected_pot.plant.watering)
            cu.place_component(lbl_plant_watering_value, 6, 3)


        tabs.add(self.selected_pot_area, text="Pot Info")


        #EDIT POT TAB
        edit_tab = ttk.Labelframe(tabs)
        change_name = CustomEntry(edit_tab, 0, 0, "Enter new pot name: ", selected_pot.pot_tk.name)

        edit_btn = ttk.Button(edit_tab, text="Update", command=lambda: self.edit_pot(selected_pot))
        edit_btn.grid(row=0, column=3, padx=5, pady=5, sticky=tk.N)

        empty_pot_lbl = ttk.Label(edit_tab, text=f"Empty '{selected_pot.name}' pot?")
        empty_pot_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)

        empty_btn = tk.Button(edit_tab, text="Empty", command=lambda: self.empty_pot(selected_pot))
        empty_btn.grid(row=1, column=1, padx=5, pady=5, sticky=tk.N)

        delete_pot_lbl = ttk.Label(edit_tab, text=f"Delete '{selected_pot.name}' pot?")
        delete_pot_lbl.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N)

        delete_btn = tk.Button(edit_tab, text="Delete", bg="red", command=lambda: self.delete_pot(selected_pot))
        delete_btn.grid(row=2, column=1, padx=5, pady=5, sticky=tk.N)
        tabs.add(edit_tab, text="Edit Pot")


        #PLANT TAB
        self.plant_tab = ttk.Labelframe(tabs)
        self.available_plants(selected_pot)
        tabs.add(self.plant_tab, text="Choose a plant")

        self.scale_area(selected_pot)

        #GRAPH TAB
        graph_tab = ttk.LabelFrame(tabs)
        self.radio_options = IntVar()
        line_graph = ttk.Radiobutton(graph_tab, text="Line graph", variable=self.radio_options, value=0)
        cu.place_component(line_graph, 0, 0, tk.W)

        pie_graph = ttk.Radiobutton(graph_tab, text="Pie graph", variable=self.radio_options, value=1)
        cu.place_component(pie_graph, 1, 0, tk.W)

        histogram = ttk.Radiobutton(graph_tab, text="Histogram", variable=self.radio_options, value=2)
        cu.place_component(histogram, 2, 0, tk.W)

        self.graphs_btn = ttk.Button(graph_tab, text="Show graph", command=lambda: self.open_graphs_window(selected_pot))
        cu.place_component(self.graphs_btn, 3, 0, tk.W)

        tabs.add(graph_tab, text="Graphs")

    def close(self):
        self.destroy()
        self.parent.grid()


    def make_pot(self):
        name = self.new_pot.get()
        img = "./images/pot.png"
        if name is not None and name != "":
            self.repo.add_pot(name, img)
            self.destroy()
            PotScreen(self.parent, self.db)

        else:
            tk.messagebox.showinfo("Name field empty", "Please enter the name of the pot.")



    def delete_pot(self, selected_pot):
        msg_box = tk.messagebox.askquestion('Delete Pot', f"Are you sure you want to delete '{selected_pot.name}' pot?",
                                            icon='warning')
        if msg_box == 'yes':
            self.repo.delete_pot(selected_pot)
            self.destroy()
            PotScreen(self.parent, self.db)

    def empty_pot(self, selected_pot):
        msg_box = tk.messagebox.askquestion('Empty Pot', f"Are you sure you want to empty '{selected_pot.name}' pot?",
                                            icon='warning')
        if msg_box == 'yes':
            selected_pot.pot_img = "./images/pot.png"
            self.repo.empty_pot(selected_pot)
            self.destroy()
            PotScreen(self.parent, self.db)

    def edit_pot(self, selected_pot):
        selected_pot.name = selected_pot.pot_tk.name.get()
        self.repo.update_pot(selected_pot)
        self.destroy()
        PotScreen(self.parent, self.db)



    def available_plants(self, selected_pot):
        row = 1
        column = 0

        fetch_plants = self.repo_plant.find_all_plants()

        for plant in fetch_plants:

            plant_preview = ttk.LabelFrame(self.plant_tab)
            cu.place_component(plant_preview, row, column)

            plant_name = ttk.Label(plant_preview, text=plant.name)
            cu.place_component(plant_name, 0, 0, tk.EW)
            plant_name.bind("<Button-1>",
                            lambda event, selected_plant=plant: self.plant_into_pot(selected_pot, selected_plant))
            plant_image = FileUtil.work_on_img(plant.plant_image, 50, 50)
            plant_preview_img = tk.Label(plant_preview, image=plant_image)
            plant_preview_img.image = plant_image
            cu.place_component(plant_preview_img, 0, 1)
            plant_preview_img.bind("<Button-1>", lambda event, selected_plant=plant: self.plant_into_pot(selected_pot,
                                                                                                          selected_plant))

            column += 1
            if column == 3:
                row += 1
                column = 0
            if row == 4 and column == 1:
                show_all_btn = tk.Button(self.plant_tab, text="Show All Plants", command=lambda: self.too_many_plants(selected_pot))
                show_all_btn.grid(row=4, column=1, padx=5, pady=5)
                break


    def plant_into_pot(self, selected_pot, selected_plant):
        if selected_pot.plant_id is None:
            msg_box1 = tk.messagebox.askquestion('Plant a new plant',
                                                f"Are you sure you want to plant '{selected_plant.name}' into '{selected_pot.name}' pot?",
                                                icon='warning')
            if msg_box1 == 'yes':
                selected_pot.pot_img = selected_plant.plant_image
                selected_pot.plant_id = selected_plant.id
                self.repo.update_pot(selected_pot, True)
                self.destroy()
                PotScreen(self.parent, self.db)

        else:
            msg_box2 = tk.messagebox.askquestion('Replace a plant', f"Are you sure you want to plant another plant in '{selected_pot.name}' pot?",
                                                icon='warning')
            if msg_box2 == 'yes':
                selected_pot.watering_date = dt.now().timestamp()
                selected_pot.pot_img = selected_plant.plant_image
                selected_pot.plant_id = selected_plant.id
                self.repo.update_pot(selected_pot, True)
                self.destroy()
                PotScreen(self.parent, self.db)


    def set_status_imgs(self, selected_pot: PotDto):
        values = self.repo_values.fetch_all_values(selected_pot.id, selected_pot.plant_id)
        if values is not None:
            if values.ph_value >= selected_pot.plant.plant_ph_low and values.ph_value <= selected_pot.plant.plant_ph_high:
                self.pot_ph_status_preview.config(image=self.status_ok)
            elif values.ph_value < selected_pot.plant.plant_ph_low:
                self.pot_ph_status_preview.config(image=self.status_acid)
            elif values.ph_value > selected_pot.plant.plant_ph_high:
                self.pot_ph_status_preview.config(image=self.status_alkaline)
            if values.sunlight_value >= selected_pot.plant.sunlight_low and values.sunlight_value <= selected_pot.plant.sunlight_high:
                self.pot_sun_status_preview.config(image=self.status_ok)
            elif values.sunlight_value < selected_pot.plant.sunlight_low:
                self.pot_sun_status_preview.config(image=self.status_sun)
            elif values.sunlight_value > selected_pot.plant.sunlight_high:
                self.pot_sun_status_preview.config(image=self.status_moon)
            if values.temperature_value >= selected_pot.plant.temperature_low and values.temperature_value <= selected_pot.plant.temperature_high:
                self.pot_temperature_status_preview.config(image=self.status_ok)
            elif values.temperature_value < selected_pot.plant.temperature_low:
                self.pot_temperature_status_preview.config(image=self.status_temp_low)
            elif values.temperature_value > selected_pot.plant.temperature_high:
                self.pot_temperature_status_preview.config(image=self.status_temp_high)

            if values.watering is not None:
                converted_time = dt.strptime(values.watering, '%Y-%m-%d %H:%M:%S.%f')
                self.watering_time = dt.now() - converted_time

                if self.watering_time.days <= selected_pot.plant.watering:
                    self.pot_watering_status_preview.config(image=self.status_ok)
                elif self.watering_time.days > selected_pot.plant.watering:
                    self.pot_watering_status_preview.config(image=self.status_dry)


    def scale_area(self, selected_pot):

        self.scales_container = ttk.Labelframe(self.pot_info_area, text="Scales")
        cu.place_component(self.scales_container, 0, 2)

        self.ph_value_scale = CustomScale(self.scales_container, 0, 0, "pH value", (0, 14), 1)
        self.sunlight_scale = CustomScale(self.scales_container, 1, 0, "Hours of sunlight needed(h)", (0, 24), 0)
        self.temp_scale = CustomScale(self.scales_container, 2, 0, "Temperature(c°)", (-10, 40), 0)

        self.watering_time = ttk.Checkbutton(self.scales_container,
                                        text="Water the plant",
                                        variable=selected_pot.pot_tk.water)
        cu.place_component(self.watering_time, 3, 0, tk.W)

        self.btn_sync = ttk.Button(self.scales_container, text="Sync", command=lambda: self.sync_data(selected_pot))
        cu.place_component(self.btn_sync, 3, 1)





    def sync_data(self, selected_pot):
        if selected_pot.plant is not None:
            ph_value = self.ph_value_scale.value.get()
            sunlight_value = self.sunlight_scale.value.get()
            temperature_value = self.temp_scale.value.get()
            plant_id = selected_pot.plant_id
            pot_id = selected_pot.id

            if selected_pot.pot_tk.water.get() == True:
                water = dt.now()
                self.repo_values.add_values(ph_value, sunlight_value, temperature_value, water, plant_id, pot_id)
                self.destroy()
                PotScreen(self.parent, self.db)

            else:
                water = self.repo_values.get_old_watering_date(selected_pot.id, selected_pot.plant_id)
                if water is None:
                    water = dt.now()

                self.repo_values.add_values(ph_value, sunlight_value, temperature_value, water, plant_id, pot_id)

            tk.messagebox.showinfo("Values saved!", "Values have been saved successfully!")

        else:
            tk.messagebox.showinfo("Empty pot", "Can't save values from an empty pot")

    def load_images(self):
        self.status_ok = FileUtil.work_on_img("./images/status_img/ok.png", 15, 15)
        self.status_acid = FileUtil.work_on_img("./images/status_img/acid.png", 15, 15)
        self.status_alkaline = FileUtil.work_on_img("./images/status_img/alkaline.png", 15, 15)
        self.status_sun = FileUtil.work_on_img("./images/status_img/sun.png", 15, 15)
        self.status_moon = FileUtil.work_on_img("./images/status_img/moon.png", 15, 15)
        self.status_temp_low = FileUtil.work_on_img("./images/status_img/temp_low.png", 15, 15)
        self.status_temp_high = FileUtil.work_on_img("./images/status_img/temp_high.png", 15, 15)
        self.status_dry = FileUtil.work_on_img("./images/status_img/dry.png", 15, 15)

    def too_many_plants(self, selected_pot):
        new_window = tk.Toplevel(self)
        new_window.title("Chose a plant window")
        row = 1
        column = 0
        fetch_plants = self.repo_plant.find_all_plants()

        for plant in fetch_plants:

            plant_preview = ttk.LabelFrame(new_window)
            cu.place_component(plant_preview, row, column)

            plant_name = ttk.Label(plant_preview, text=plant.name)
            cu.place_component(plant_name, 0, 0, tk.EW)
            plant_name.bind("<Button-1>", lambda event, selected_plant=plant: self.plant_into_pot(selected_pot, selected_plant))
            plant_image = FileUtil.work_on_img(plant.plant_image, 50, 50)
            plant_preview_img = tk.Label(plant_preview, image=plant_image)
            plant_preview_img.image = plant_image
            cu.place_component(plant_preview_img, 0, 1)
            plant_preview_img.bind("<Button-1>", lambda event, selected_plant=plant: self.plant_into_pot(selected_pot, selected_plant))

            column += 1
            if column == 5:
                row += 1
                column = 0



    def open_graphs_window(self, selected_pot: PotDto):
        if selected_pot.plant_id is not None:
            radio_value = self.radio_options.get()
            ph_values = []
            sun_values = []
            temp_values = []
            values = self.repo_values.fetch_all_values(selected_pot.id, selected_pot.plant_id, False)
            if values is not None:
                if len(values) > 1:

                    for item in values:
                        ph_values.append(item.ph_value)
                        sun_values.append(item.sunlight_value)
                        temp_values.append(item.temperature_value)

                        self.y_ph_value = ph_values
                        self.y_sun_value = sun_values
                        self.y_temp_value = temp_values

                    if radio_value == 0:

                        x_length = max(len(self.y_ph_value), len(self.y_sun_value), len(self.y_temp_value))
                        x_values = list(range(1, x_length + 1))

                        plt.plot(x_values[:len(self.y_ph_value)], self.y_ph_value, marker='o', linestyle='-', label='pH value')
                        plt.plot(x_values[:len(self.y_sun_value)], self.y_sun_value, marker='o', linestyle='-', label='sunlight value')
                        plt.plot(x_values[:len(self.y_temp_value)], self.y_temp_value, marker='o', linestyle='-', label='temperature value')


                        plt.xlabel('x-axis')
                        plt.ylabel('Values')
                        plt.title('Selected pot values line chart')

                        plt.legend()
                        plt.show()

                    if radio_value == 1:
                        plt.figure(figsize=(15, 5))

                        ph_pie = self.y_ph_value
                        sun_pie = self.y_sun_value
                        temp_pie = self.y_temp_value

                        plt.subplot(131)
                        plt.pie(ph_pie, autopct='%d', startangle=90)
                        plt.title('Pie Chart for pH values')

                        plt.subplot(132)
                        plt.pie(sun_pie, autopct='%d', startangle=90)
                        plt.title('Pie Chart for Sunlight values')

                        plt.subplot(133)
                        plt.pie(temp_pie, autopct='%d', startangle=90)
                        plt.title('Pie Chart for Temperature values')
                        plt.show()

                    if radio_value == 2:
                        plt.figure(figsize=(15, 5))

                        plt.subplot(131)
                        plt.hist(self.y_ph_value, bins=10, edgecolor='black', color="green")
                        plt.xlabel('pH')
                        plt.ylabel('Frequency')
                        plt.title('pH Values')

                        plt.subplot(132)
                        plt.hist(self.y_sun_value, bins=10, edgecolor='black', color="red")
                        plt.xlabel('Days')
                        plt.ylabel('Frequency')
                        plt.title('Sunlight Values')

                        plt.subplot(133)
                        plt.hist(self.y_temp_value, bins=10, edgecolor='black', color="blue")
                        plt.xlabel('C°')
                        plt.ylabel('Frequency')
                        plt.title('Temperature Values')

                        plt.tight_layout()
                        plt.show()


                else:
                    tk.messagebox.showinfo("Graphs are not available", "More data needed to make graphs.")

















