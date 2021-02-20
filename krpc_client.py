import krpc


class KRPCClient:

    def __init__(self):
        self.client = krpc.connect(name="test", address='0.0.0.0', rpc_port=1000, stream_port=1001)
        self.vessel = self.client.space_center.active_vessel
        self.srf_frame = self.vessel.orbit.body.reference_frame
        self.altitude = 0
        self.fuel = self.vessel.resources

    def toggle_sas(self):
        self.vessel.control.sas = not self.vessel.control.sas

    def toggle_gears(self):
        self.vessel.control.gears = not self.vessel.control.gears

    def toggle_brakes(self):
        self.vessel.control.brakes = not self.vessel.control.brakes

    def toggle_auto(self):
        pitch = self.vessel.control.pitch
        if pitch != -1:
            pitch = -1
        else:
            pitch = 0
        self.vessel.control.pitch = pitch

    def next_stage(self):
        self.vessel.control.activate_next_stage()

    def auto_trim(self):
        self.altitude = self.vessel.flight().surface_altitude

    def set_throttle(self, slider):
        self.vessel.control.throttle = slider['value']

    def set_pitch(self, slider):
        self.vessel.control.pitch = slider['value']

    def set_roll(self, slider):
        self.vessel.control.roll = slider['value']

    def set_yaw(self, slider):
        self.vessel.control.yaw = slider['value']

    def get_fuel(self):
        return self.fuel.amount('LiquidFuel')

    def get_speed(self):
        return self.vessel.flight(self.srf_frame).speed

    def get_altitude(self):
        return self.vessel.flight().surface_altitude
