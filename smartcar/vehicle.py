from .api import Api

class Vehicle(object):
    def __init__(self, vehicle_id, access_token, imperial=False):
        self.vehicle_id = vehicle_id
        self.access_token = access_token
        self.api = Api(access_token, vehicle_id)
        self.api.set_unit('imperial' if imperial else 'metric')
    def set_unit(self, unit):
        if unit not in ('metric','imperial'):
            raise ValueError("unit must be either metric or imperial")
        else:
            self.api.set_unit(unit)
    def permissions(self, limit=25, offset=0):
        return self.api.permissions(limit=limit, offset=offset)
    def info(self):
        return self.api.get("")
    def accelerometer(self):
        return self.api.get("accelerometer")
    def airbags(self):
        return self.api.get("airbags")
    def barometer(self):
        return self.api.get("barometer")
    def battery(self):
        return self.api.get("battery")
    def charge(self):
        return self.api.get("charge")
    def charge_limit(self):
        return self.api.get("charge/limit")
    def charge_schedule(self):
        return self.api.get("charge/schedule")
    def climate(self):
        return self.api.get("climate")
    def collision_sensor(self):
        return self.api.get("collision_sensor")
    def compass(self):
        return self.api.get("compass")
    def cruise_control(self):
        return self.api.get("cruise_control")
    def dimension(self):
        return self.api.get("dimensions")
    def doors(self):
        return self.api.get("doors")
    def child_safety_locks(self):
        return self.api.get("doors/child_safety_locks")
    def drive_mode(self):
        return self.api.get("drive_mode")
    def engine(self):
        return self.api.get("engine")
    def engine_coolant(self):
        return self.api.get("engine/coolant")
    def engine_hood(self):
        return self.api.get("engine/hood")
    def engine_oil(self):
        return self.api.get("engine/oil")
    def engine_throttle(self):
        return self.api.get("engine/throttle")
    def fuel(self):
        return self.api.get("fuel")
    def gyroscope(self):
        return self.api.get("gyroscope")
    def ignition(self):
        return self.api.get("ignition")
    def hazard_light(self):
        return self.api.get("lights/hazard")
    def headlights(self):
        return self.api.get("lights/headlights")
    def interior_lights(self):
        return self.api.get("lights/interior")
    def turn_indicator(self):
        return self.api.get("lights/turn_indicator")
    def location(self):
        return self.api.get("location")
    def side_view_mirrors(self):
        return self.api.get("mirrors/side_view")
    def odometer(self):
        return self.api.get("odometer")
    def trip_odometers(self):
        return self.api.get("odometer/trips")
    def accelerator_pedal(self):
        return self.api.get("pedals/accelerator")
    def brake_pedal(self):
        return self.api.get("pedals/brake")
    def rain_sensor(self):
        return self.api.get("rain_sensor")
    def seats(self):
        return self.api.get("seats")
    def security(self):
        return self.api.get("security")
    def sli_battery(self):
        return self.api.get("sli_battery")
    def speedometer(self):
        return self.api.get("speedometer")
    def steering_wheel(self):
        return self.api.get("steering_wheel")
    def sunroof(self):
        return self.api.get("sunroof")
    def tachometer(self):
        return self.api.get("tachometer")
    def interior_thermistor(self):
        return self.api.get("thermistors/interior")
    def exterior_thermistor(self):
        return self.api.get("thermistors/exterior")
    def tires(self):
        return self.api.get("tires")
    def transmission(self):
        return self.api.get("transmission")
    def transmission_fluid(self):
        return self.api.get("transmission/fluid")
    def front_trunk(self):
        return self.api.get("trunks/front")
    def rear_trunk(self):
        return self.api.get("trunks/rear")
    def vin(self):
        return self.api.get("vin");
    def washer_fluid(self):
        return self.api.get("washer_fluid")
    def wheels(self):
        return self.api.get("wheels")
    def wheel_speeds(self):
        return self.api.get("wheels/speeds")
    def windows(self):
        return self.api.get("windows")


    # Actions
    def disconnect(self):
        return self.api.disconnect()
    def start_charging(self):
        return self.api.action("charge", "START")
    def stop_charging(self):
        return self.api.action("charge", "STOP")
    def enable_charge_limit(self,limit=None):
        return self.api.action("charge/limit", "ENABLE", limit=limit)
    def disable_charge_limit(self):
        return self.api.action("charge/limit", "DISABLE")
    def enable_charge_schedule(self,startTime=None):
        return self.api.action("charge/schedule", "ENABLE", startTime=startTime)
    def disable_charge_schedule(self):
        return self.api.action("charge/schedule", "DISABLE")
    def activate_safety_locks(self, child_safety_locks=None):
        return self.api.action("doors/child_safety_locks", "LOCK", child_safety_locks=child_safety_locks)
    def disable_safety_locks(self, child_safety_locks=None):
        return self.api.action("doors/child_safety_locks", "UNLOCK", child_safety_locks=child_safety_locks)
    def start_climate(self, temperature=None):
        return self.api.action("climate", "START", temperature=temperature)
    def stop_climate(self):
        return self.api.action("climate", "STOP")
    def open_engine_hood(self):
        return self.api.action("engine/hood", "OPEN")
    def close_engine_hood(self):
        return self.api.action("engine/hood", "CLOSE")
    def start_ignition(self):
        return self.api.action("ignition", "START")
    def set_ignition_on(self):
        return self.api.action("ignition", "ON")
    def set_ignition_accessory(self):
        return self.api.action("ignition", "ACCESSORY")
    def set_ignition_off(self):
        return self.api.action("ignition", "OFF")
    def honk_horn(self):
        return self.api.action("horn", "HONK")
    def flash_headlights(self, type=None):
        return self.api.action("lights/headlights", "FLASH", type=type)
    def tilt_sideview_mirrors(self, mirrors):
        return self.api.action("mirrors/side_view", "TILT", mirrors=mirrors)
    def start_panic(self):
        return self.api.action("panic", "START")
    def stop_panic(self):
        return self.api.action("panic", "STOP")
    def open_charge_port(self):
        return self.api.action("ports/charge", "OPEN")
    def close_charge_port(self):
        return self.api.action("ports/charge", "CLOSE")
    def open_fuel_port(self):
        return self.api.action("ports/fuel", "OPEN")
    def close_fuel_port(self):
        return self.api.action("ports/fuel", "CLOSE")
    def lock(self):
        return self.api.action("security", "LOCK")
    def unlock(self):
        return self.api.action("security", "UNLOCK")
    def open_sunroof(self):
        return self.api.action("sunroof", "OPEN")
    def vent_sunroof(self):
        return self.api.action("sunroof", "VENT")
    def close_sunroof(self):
        return self.api.action("sunroof", "CLOSE")
    def open_front_trunk(self):
        return self.api.action("trunks/front", "OPEN")
    def close_front_trunk(self):
        return self.api.action("trunks/front", "CLOSE")
    def open_rear_trunk(self):
        return self.api.action("trunks/rear", "OPEN")
    def close_rear_trunk(self):
        return self.api.action("trunks/rear", "CLOSE")
    def open_windows(self, windows):
        return self.api.action("windows", "OPEN", windows=windows)
    def close_windows(self, windows):
        return self.api.action("windows", "CLOSE", windows=windows)
    def lock_windows(self, windows):
        return self.api.action("windows", "LOCK", windows=windows)
    def unlock_windows(self, windows):
        return self.api.action("windows", "UNLOCK", windows=windows)
