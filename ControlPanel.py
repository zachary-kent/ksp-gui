import tkinter as tk
from tkinter import ttk
from krpc_client import KRPCClient


class ControlPanel:

    def __init__(self, width=350, height=350):
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.bg_color = "black"
        self.text_color = "white"
        self.sliders = list()
        self.client = KRPCClient()
        self.__screen_init__()
        self.__label_init__()
        self.__slider_init__()
        self.__progress_bar_init__()
        self.__button_init__()

    def __screen_init__(self):
        self.root.geometry(str(self.width) + "x" + str(self.height))
        self.root.resizable(0, 0)
        back = tk.Frame(master=self.root, bg='black')
        back.pack_propagate(0)
        back.pack(fill=tk.BOTH, expand=1)

    def __slider_init__(self):
        self.throttle_slider = self.__slider__('vertical')
        self.roll_slider = self.__slider__('horizontal')
        self.yaw_slider = self.__slider__('horizontal')
        self.pitch_slider = self.__slider__('horizontal')
        self.throttle_slider.place(x=0.24 * self.width, y=0.18 * self.height)
        self.roll_slider.place(x=0.14 * self.width, y=0.5 * self.height)
        self.yaw_slider.place(x=0.14 * self.width, y=0.55 * self.height)
        self.pitch_slider.place(x=0.14 * self.width, y=0.6 * self.height)

    def __label_init__(self):
        altitude_label = self.__label__("Altitude (m):")
        speed_label = self.__label__("Speed (m/s):")
        altitude_label.place(x=self.width * 0.02, y=0.035 * self.height)
        speed_label.place(x=self.width * 0.02, y=0.1 * self.height)
        self.altitude_value_label = self.__label__("0")
        self.speed_value_label = self.__label__("0")
        self.altitude_value_label.place(x=self.width * 0.2, y=0.035 * self.height)
        self.speed_value_label.place(x=self.width * 0.2, y=0.1 * self.height)
        fuel_label = self.__label__("Fuel:")
        throttle_label = self.__label__("Throttle:")
        fuel_label.place(x=self.width / 50, y=0.4 * self.height)
        throttle_label.place(x=0.19 * self.width, y=0.4 * self.height)
        roll_label = self.__label__("Roll:")
        yaw_label = self.__label__("Yaw:")
        pitch_label = self.__label__("Pitch:")
        roll_label.place(x=self.width / 50, y=0.5 * self.height)
        yaw_label.place(x=self.width / 50, y=0.55 * self.height)
        pitch_label.place(x=self.width / 50, y=0.6 * self.height)

    def __progress_bar_init__(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure(style="y.Vertical.TProgressbar", troughcolor='black', background='yellow')
        self.fuel_bar = ttk.Progressbar(master=self.root, style="y.Vertical.TProgressbar", orient='vertical', length=100)
        self.fuel_bar['maximum'] = 1
        self.fuel_bar.place(x=self.width * 0.04, y=0.18 * self.height)

    def __button_init__(self):
        '''
        button_frame = tk.Frame(master=self.root, height=self.height / 5, borderwidth=0.055 * self.width, relief='solid', bg=self.bg_color)
        button_frame.place(x=self.width / 2, y=self.height / 2)
        button_frame.pack()
        '''
        auto_button = tk.Button(master=self.root, text="Autopilot", command=self.client.toggle_auto)
        auto_button.place(x=self.width / 1.6, y=self.height * 0.4)
        brakes_button = tk.Button(master=self.root, text="Toggle Brakes", command=self.client.toggle_brakes)
        brakes_button.place(x=self.width / 1.6, y=self.height * 0.5)
        sas_button = tk.Button(master=self.root, text="SAS", command=self.client.toggle_sas)
        sas_button.place(x=self.width / 1.6, y=self.height * 0.6)
        gears_button = tk.Button(master=self.root, text="Landing Gear", command=self.client.toggle_gears)
        gears_button.place(x=self.width / 1.6, y=self.height * 0.7)

    def __label__(self, label_text):
        return tk.Label(master=self.root, text=label_text, fg=self.text_color, bg=self.bg_color)

    def __slider__(self, orient):
        slider = ttk.Scale(master=self.root, length=100, orient=orient)
        slider['from'] = 1.0
        slider['to'] = 0.0
        return slider

    def run(self):
        self.root.mainloop()
        self.root.after(1, self.root.update())
        while True:
            self.client.set_pitch(self.pitch_slider)
            self.client.set_roll(self.roll_slider)
            self.client.set_throttle(self.throttle_slider)
            self.client.set_yaw(self.yaw_slider)
            self.fuel_bar['value'] = self.client.get_fuel()
            self.speed_value_label.config(text=str(round(self.client.get_speed(), 2)))
            self.altitude_value_label.config(text=str(round(self.client.get_altitude(), 2)))


if __name__ == "__main__":
    cp = ControlPanel(500, 500)
    cp.run()
