import krpc
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.geometry("350x380")
root.resizable(0, 0)

back = tk.Frame(master=root, bg='black')
back.pack_propagate(0)
back.pack(fill=tk.BOTH, expand=1)

x = 110
y = 10

c = krpc.connect(name="test", address='0.0.0.0', rpc_port=1000, stream_port=1001)
v = c.space_center.active_vessel

srf_frame = v.orbit.body.reference_frame
obt_frame = v.orbit.body.non_rotating_reference_frame

stage1_fuel = v.resources

ap = v.auto_pilot
ap.reference_frame = v.surface_reference_frame


class ksp_init():
    def __init__(self):
        self.stop = False
        self.current = 0
        self.i = 0
        self.i1 = 0
        self.i2 = 0
        self.i3 = 0
        self.i4 = 0
        self.i5 = 0
        self.i6 = 0

    def sas(self):
        if (self.i1 == 0):
            v.control.sas = True
            self.i1 = 1
        elif (self.i1 == 1):
            v.control.sas = False
            self.i1 = 0

    def gears(self):
        if (self.i == 0):
            v.control.gear = False
            self.i = 1
        elif (self.i == 1):
            v.control.gear = True
            self.i = 0

    def brakes(self):
        if (self.i2 == 0):
            v.control.brakes = False
            self.i2 = 1
        elif (self.i2 == 1):
            v.control.brakes = True
            self.i2 = 0

    def stage(self):
        v.control.activate_next_stage()

    def Disengage(self):
        self.i5 = 1
        print(self.i5)

    def auto_takeoff(self):
        self.i3 = 1

    def auto_trim(self):
        self.current = v.flight().surface_altitude
        print(self.current)
        self.i4 = 1
        self.i5 = 0

    def q(self):
        self.stop = True

    def ksp_pull(self, spd_l, alt_l, t_l, f_l, throt_b, fuel_b, throt_c, roll_b, roll_l, yaw_b, yaw_l, pitch_b, pitch_l,
                 roll_b1, yaw_b1, pitch_b1):
        while not self.stop:

            throt_b["value"] = v.control.throttle
            fuel_b["value"] = stage1_fuel.amount('LiquidFuel')

            roll_b["value"] = v.control.roll
            roll_b1["value"] = v.control.roll
            yaw_b["value"] = v.control.yaw
            yaw_b1["value"] = v.control.yaw
            pitch_b["value"] = v.control.pitch
            pitch_b1["value"] = v.control.pitch

            t_l.config(text=str(round(v.control.throttle, 2)))

            f_l.config(text=str(round(stage1_fuel.amount('LiquidFuel'))))

            spd_l.config(text=str(round(v.flight(srf_frame).speed, 2)))
            alt_l.config(text=str(round(v.flight().surface_altitude, 2)))

            roll_l.config(text=str(round(v.control.roll, 2)))
            yaw_l.config(text=str(round(v.control.yaw, 2)))
            pitch_l.config(text=str(round(v.control.pitch, 2)))

            root.after(1, root.update())

            v.control.throttle = throt_c.get()
            time.sleep(0.05)
            throt_c.set(v.control.throttle)

            if (self.i3 == 1):
                if (v.flight().surface_altitude < 70):
                    self.brakes()
                    self.i2 = 0
                    v.control.pitch = 0.6
                    v.control.throttle = 1

                elif (v.flight().surface_altitude >= 445):
                    v.control.pitch = 0.2
                    v.control.pitch = 0
                    v.control.throttle = 0.5
                    self.gears()
                    self.sas()
                    self.i = 1
                    self.i3 = 0

                else:
                    v.control.pitch = 0

            if (self.i4 == 1):
                if (self.i5 == 0):
                    if (v.flight().surface_altitude < self.current + 10):
                        v.control.pitch = 0.2
                        self.sas()
                        self.i1 = 1

                    elif (v.flight().surface_altitude > self.current + 50):
                        v.control.pitch = -0.05
                        self.sas()
                        self.i1 = 1

                    else:
                        v.control.pitch = 0
                        self.i1 = 0
                        self.sas()
                else:
                    self.i5 = 0
                    self.i4 = 0
                    self.i1 = 0
                    self.sas()

        root.destroy()

    def ui(self):
        frame = Frame(root, height=20, borderwidth=2, relief="solid", bg="white")
        frame.pack()
        frame.place(x=x, y=y)

        alt_label = tk.Label(frame, fg="black", bg="white")
        alt_label.pack(anchor=W)

        alt_label1 = tk.Label(root, fg="white", bg="black", text="Altidude (metters):", width=14, height=0, anchor=W)
        alt_label1.place(x=x - 110, y=y)

        ############################################################################# END OF ALT DISPLAY

        frame1 = Frame(root, width=200, height=20, borderwidth=2, relief="solid", bg="white")
        frame1.pack()
        frame1.place(x=x, y=y + 25)

        spd_label = tk.Label(frame1, fg="black", bg="white")
        spd_label.pack(anchor=W)

        spd_label1 = tk.Label(root, fg="white", bg="black", text="speed (m/s):", width=14, height=0, anchor=E)
        spd_label1.place(x=x - 110, y=y + 25)
        ############################################################################# END OF SPD DISPLAY

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("y.Vertical.TProgressbar", troughcolor='black', background='yellow')

        s1 = ttk.Style()
        s1.theme_use('clam')
        s1.configure("y.Horizontal.TProgressbar", troughcolor='black', background='yellow')
        ############################################################################# END OF THEME FOR BARS

        fuel_bar = ttk.Progressbar(root, style="y.Vertical.TProgressbar", orient="vertical", length=100,
                                   mode="determinate")
        fuel_bar.place(x=10, y=y + 60)
        fuel_bar["maximum"] = stage1_fuel.amount('LiquidFuel')

        f_l = tk.Label(root, fg="white", bg="black", text="fuel:", anchor=W)
        f_l.place(x=5, y=y + 165)
        f_l1 = tk.Label(root, fg="white", bg="black", anchor=E)
        f_l1.place(x=33, y=y + 165)
        ############################################################################# END OF FUEL BAR

        throt_bar = ttk.Progressbar(root, style="y.Vertical.TProgressbar", orient="vertical", length=100,
                                    mode="determinate")
        throt_bar.place(x=80, y=y + 60)
        throt_bar["maximum"] = 1

        t_l = tk.Label(root, fg="white", bg="black", text="throttle:", anchor=W)
        t_l.place(x=75, y=y + 165)
        t_l1 = tk.Label(root, fg="white", bg="black", anchor=E)
        t_l1.place(x=123, y=y + 165)

        ############################################################################# END OF THROTTLE BAR

        throt_control = ttk.Scale(root, from_=1.0, to=0.0, length=100, orient='vertical')
        throt_control['to'] = 0.0
        throt_control['from'] = 1.0

        throt_control.place(x=100, y=y + 60)

        #   ############################################################################ END OF THROTTLE CONTROL

        roll_bar = ttk.Progressbar(root, style="y.Horizontal.TProgressbar", orient="horizontal", length=50,
                                   mode="determinate")
        roll_bar.place(x=x - 10, y=y + 190)
        roll_bar["maximum"] = -1

        roll_bar1 = ttk.Progressbar(root, style="y.Horizontal.TProgressbar", orient="horizontal", length=50,
                                    mode="determinate")
        roll_bar1.place(x=x + 40, y=y + 190)
        roll_bar1["maximum"] = 1

        r_l = tk.Label(root, fg="white", bg="black", text="Roll:", anchor=W)
        r_l.place(x=5, y=y + 190)
        r_l1 = tk.Label(root, fg="white", bg="black", anchor=E)
        r_l1.place(x=33, y=y + 190)

        yaw_bar = ttk.Progressbar(root, style="y.Horizontal.TProgressbar", orient="horizontal", length=50,
                                  mode="determinate")
        yaw_bar.place(x=x - 10, y=y + 230)
        yaw_bar["maximum"] = -1
        yaw_bar1 = ttk.Progressbar(root, style="y.Horizontal.TProgressbar", orient="horizontal", length=50,
                                   mode="determinate")
        yaw_bar1.place(x=x + 40, y=y + 230)
        yaw_bar1["maximum"] = 1

        y_l = tk.Label(root, fg="white", bg="black", text="Yaw:", anchor=W)
        y_l.place(x=5, y=y + 230)
        y_l1 = tk.Label(root, fg="white", bg="black", anchor=E)
        y_l1.place(x=33, y=y + 230)

        pitch_bar = ttk.Progressbar(root, style="y.Vertical.TProgressbar", orient="vertical", length=30,
                                    mode="determinate")
        pitch_bar.place(x=x + 100, y=y + 190)
        pitch_bar["maximum"] = 1
        pitch_bar1 = ttk.Progressbar(root, style="y.Vertical.TProgressbar", orient="vertical", length=30,
                                     mode="determinate")
        pitch_bar1.place(x=x + 100, y=y + 220)
        pitch_bar1["maximum"] = -1

        p_l = tk.Label(root, fg="white", bg="black", text="Pitch:", anchor=W)
        p_l.place(x=x + 125, y=y + 210)
        p_l1 = tk.Label(root, fg="white", bg="black", anchor=E)
        p_l1.place(x=x + 160, y=y + 210)

        ############################################################################# END OF pitch,roll,yaw

        frame1 = Frame(root, width=242, height=70, borderwidth=2, relief="sunken", bg="black",
                       highlightbackground="white", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=y + 263)

        q = Button(root, text="Quit", command=(lambda: self.q()))
        q.place(x=5, y=y + 300)

        at = Button(root, text="Auto Take Off", command=(lambda: self.auto_takeoff()))
        at.place(x=45, y=y + 300)

        al = Button(root, text="Auto Level", command=(lambda: self.auto_trim()))
        al.place(x=135, y=y + 300)

        s = Button(root, text="SAS", command=(lambda: self.sas()))
        s.place(x=205, y=y + 300)

        g = Button(root, text="Gears", command=(lambda: self.gears()))
        g.place(x=5, y=y + 270)

        st = Button(root, text="Stage", command=(lambda: self.stage()))
        st.place(x=50, y=y + 270)

        br = Button(root, text="Brakes", command=(lambda: self.brakes()))
        br.place(x=95, y=y + 270)

        dis = Button(root, text="Disengage", command=(lambda: self.Disengage()))
        dis.place(x=145, y=y + 270)

        ############################################################################# END OF BUTTONS (DON'T FORGET TO CHANGE THEM)

        self.ksp_pull(spd_label, alt_label, t_l1, f_l1, throt_bar, fuel_bar, throt_control, roll_bar, r_l1, yaw_bar,
                      y_l1, pitch_bar, p_l1, roll_bar1, yaw_bar1, pitch_bar1)


run = ksp_init()
run.ui()

root.mainloop()
