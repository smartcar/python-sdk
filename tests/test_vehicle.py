import unittest
import smartcar
import responses
import json

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.access_token = "access_token"
        self.vehicle_id = "vehicle_id"
        self.vehicle = smartcar.Vehicle(self.vehicle_id, self.access_token)
        self.auth = "Bearer " + self.access_token
        self.expected = { "key": "value" }

    def queue(self, method, endpoint, query=None):
        """ queue a mock response """
        url = "/".join((smartcar.const.API_URL, self.vehicle_id, endpoint))
        if query:
            query_string = "&".join(
                k + "=" + str(v) for k,v in query.items()
            )
            url += "?" + query_string

        responses.add(method, url, 
                json=self.expected, match_querystring=bool(query))

    def check(self, actual, **kwargs):
        """ 
        test that the actual response equals the expected response,
        that the "Authorization" header is the correct bearer auth string,
        and that each key in the request body is correct.
        """
        request = responses.calls[0].request
        request_auth = request.headers["Authorization"]

        self.assertEqual(actual, self.expected)
        self.assertEqual(request_auth, self.auth)

        if kwargs:
            request_json = json.loads(request.body.decode('utf-8'))
            for k,v in kwargs.items():
               self.assertEqual(request_json[k], v)
               
    @responses.activate
    def test_unit_system(self):
        self.queue("GET", "accelerometer")
        self.vehicle.accelerometer()
        unit = responses.calls[0].request.headers['unit-system']
        self.assertEqual(unit, 'metric')

        self.queue("GET", "accelerometer")
        self.vehicle.set_unit('imperial')
        self.vehicle.accelerometer()
        unit = responses.calls[1].request.headers['unit-system']
        self.assertEqual(unit, 'imperial')
        
        self.queue("POST", "climate")
        self.vehicle.set_unit('metric')
        self.vehicle.start_climate()
        unit = responses.calls[2].request.headers['unit-system']
        self.assertEqual(unit, 'metric')

    @responses.activate
    def test_permission(self):
        query = { "limit": 11, "offset": 1 } 
        self.queue("GET", "permissions", query=query)
        self.check(self.vehicle.permissions(**query))

    @responses.activate
    def test_info(self):
        self.queue("GET", "")
        self.check(self.vehicle.info())

    @responses.activate
    def test_accelerometer(self):
        self.queue("GET", "accelerometer")
        self.check(self.vehicle.accelerometer())

    @responses.activate
    def test_airbags(self):
        self.queue("GET", "airbags")
        self.check(self.vehicle.airbags())

    @responses.activate
    def test_barometer(self):
        self.queue("GET", "barometer")
        self.check(self.vehicle.barometer())

    @responses.activate
    def test_battery(self):
        self.queue("GET", "battery")
        self.check(self.vehicle.battery())

    @responses.activate
    def test_charge(self):
        self.queue("GET", "charge")
        self.check(self.vehicle.charge())

    @responses.activate
    def test_charge_limt(self):
        self.queue("GET", "charge/limit")
        self.check(self.vehicle.charge_limit())

    @responses.activate
    def test_charge_schedule(self):
        self.queue("GET", "charge/schedule")
        self.check(self.vehicle.charge_schedule())

    @responses.activate
    def test_climate(self):
        self.queue("GET", "climate")
        self.check(self.vehicle.climate())

    @responses.activate
    def test_collision_sensor(self):
        self.queue("GET", "collision_sensor")
        self.check(self.vehicle.collision_sensor())

    @responses.activate
    def test_compass(self):
        self.queue("GET", "compass")
        self.check(self.vehicle.compass())

    @responses.activate
    def test_cruise_control(self):
        self.queue("GET", "cruise_control")
        self.check(self.vehicle.cruise_control())

    @responses.activate
    def test_dimensions(self):
        self.queue("GET", "dimension")
        self.check(self.vehicle.dimensions())

    @responses.activate
    def test_doors(self):
        self.queue("GET", "doors")
        self.check(self.vehicle.doors())

    @responses.activate
    def test_safety_locks(self):
        self.queue("GET", "doors/safety_locks")
        self.check(self.vehicle.safety_locks())

    @responses.activate
    def test_drive_mode(self):
        self.queue("GET", "drive_mode")
        self.check(self.vehicle.drive_mode())

    @responses.activate
    def test_engine(self):
        self.queue("GET", "engine")
        self.check(self.vehicle.engine())

    @responses.activate
    def test_engine_coolant(self):
        self.queue("GET", "engine/coolant")
        self.check(self.vehicle.engine_coolant())

    @responses.activate
    def test_engine_hood(self):
        self.queue("GET", "engine/hood")
        self.check(self.vehicle.engine_hood())

    @responses.activate
    def test_engine_oil(self):
        self.queue("GET", "engine/oil")
        self.check(self.vehicle.engine_oil())

    @responses.activate
    def test_engine_throttle(self):
        self.queue("GET", "engine/throttle")
        self.check(self.vehicle.engine_throttle())

    @responses.activate
    def test_fuel(self):
        self.queue("GET", "fuel")
        self.check(self.vehicle.fuel())

    @responses.activate
    def test_hazard_light(self):
        self.queue("GET", "lights/hazard")
        self.check(self.vehicle.hazard_light())

    @responses.activate
    def test_headlight(self):
        self.queue("GET", "lights/headlight")
        self.check(self.vehicle.headlight())

    @responses.activate
    def test_interior_lights(self):
        self.queue("GET", "lights/interior")
        self.check(self.vehicle.interior_lights())

    @responses.activate
    def test_turn_indicator(self):
        self.queue("GET", "lights/turn_indicator")
        self.check(self.vehicle.turn_indicator())

    @responses.activate
    def test_location(self):
        self.queue("GET", "location")
        self.check(self.vehicle.location())

    @responses.activate
    def test_mirrors(self):
        self.queue("GET", "mirrors")
        self.check(self.vehicle.mirrors())

    @responses.activate
    def test_odometer(self):
        self.queue("GET", "odometer")
        self.check(self.vehicle.odometer())

    @responses.activate
    def test_trip_odometers(self):
        self.queue("GET", "odometer/trip")
        self.check(self.vehicle.trip_odometers())

    @responses.activate
    def test_accelerator_pedal(self):
        self.queue("GET", "pedals/accelerator")
        self.check(self.vehicle.accelerator_pedal())

    @responses.activate
    def test_brake_pedal(self):
        self.queue("GET", "pedals/brake")
        self.check(self.vehicle.brake_pedal())

    @responses.activate
    def test_rain_sensor(self):
        self.queue("GET", "rain_sensor")
        self.check(self.vehicle.rain_sensor())

    @responses.activate
    def test_seats(self):
        self.queue("GET", "seats")
        self.check(self.vehicle.seats())

    @responses.activate
    def test_security(self):
        self.queue("GET", "security")
        self.check(self.vehicle.security())

    @responses.activate
    def test_sli_battery(self):
        self.queue("GET", "sli_battery")
        self.check(self.vehicle.sli_battery())

    @responses.activate
    def test_speedometer(self):
        self.queue("GET", "speedometer")
        self.check(self.vehicle.speedometer())

    @responses.activate
    def test_steering_wheel(self):
        self.queue("GET", "steering_wheel")
        self.check(self.vehicle.steering_wheel())

    @responses.activate
    def test_sunroof(self):
        self.queue("GET", "sunroof")
        self.check(self.vehicle.sunroof())

    @responses.activate
    def test_tachometer(self):
        self.queue("GET", "tachometer")
        self.check(self.vehicle.tachometer())

    @responses.activate
    def test_temperature(self):
        self.queue("GET", "temperature")
        self.check(self.vehicle.temperature())

    @responses.activate
    def test_tires(self):
        self.queue("GET", "tires")
        self.check(self.vehicle.tires())

    @responses.activate
    def test_transmission(self):
        self.queue("GET", "transmission")
        self.check(self.vehicle.transmission())
    
    @responses.activate
    def test_transmission_fluid(self):
        self.queue("GET", "transmission/fluid")
        self.check(self.vehicle.transmission_fluid())

    @responses.activate
    def test_front_trunk(self):
        self.queue("GET", "trunks/front")
        self.check(self.vehicle.front_trunk())

    @responses.activate
    def test_rear_trunk(self):
        self.queue("GET", "trunks/rear")
        self.check(self.vehicle.rear_trunk())

    @responses.activate
    def test_vin(self):
        self.queue("GET", "vin")
        self.check(self.vehicle.vin())

    @responses.activate
    def test_washer_fluid(self):
        self.queue("GET", "washer_fluid")
        self.check(self.vehicle.washer_fluid())

    @responses.activate
    def test_wheels(self):
        self.queue("GET", "wheels")
        self.check(self.vehicle.wheels())

    @responses.activate
    def test_wheel_speeds(self):
        self.queue("GET", "wheels/speed")
        self.check(self.vehicle.wheel_speeds())

    @responses.activate
    def test_windows(self):
        self.queue("GET", "windows")
        self.check(self.vehicle.windows())

    @responses.activate
    def test_yaw(self):
        self.queue("GET", "yaw")
        self.check(self.vehicle.yaw())
    
    @responses.activate
    def test_disconnect(self):
        self.queue("DELETE", "application")
        self.check(self.vehicle.disconnect())
    
    @responses.activate
    def test_start_charging(self):
        self.queue("POST", "charge")
        self.check(self.vehicle.start_charging(), action="START")
    
    @responses.activate
    def test_stop_charging(self):
        self.queue("POST", "charge")
        self.check(self.vehicle.stop_charging(), action="STOP")

    @responses.activate
    def test_enable_charge_limit(self):
        self.queue("POST", "charge/limit")
        self.check(self.vehicle.enable_charge_limit(), action="ENABLE")

    @responses.activate
    def test_enable_charge_limit_with_limit(self):
        self.queue("POST", "charge/limit")
        self.check(self.vehicle.enable_charge_limit(limit=0.1),
                action="ENABLE", limit=0.1)

    @responses.activate
    def test_disable_charge_limit(self):
        self.queue("POST", "charge/limit")
        self.check(self.vehicle.disable_charge_limit(), action="DISABLE")

    @responses.activate
    def test_enable_charge_schedule(self):
        self.queue("POST", "charge/schedule")
        self.check(self.vehicle.enable_charge_schedule(), action="ENABLE")

    @responses.activate
    def test_enable_charge_schedule_with_starttime(self):
        self.queue("POST", "charge/schedule")
        self.check(self.vehicle.enable_charge_schedule(startTime="12:31"),
                action="ENABLE", startTime="12:31")

    @responses.activate
    def test_disable_charge_schedule(self):
        self.queue("POST", "charge/schedule")
        self.check(self.vehicle.disable_charge_schedule(), action="DISABLE")

    @responses.activate
    def test_start_climate(self):
        self.queue("POST", "climate")
        self.check(self.vehicle.start_climate(), action="START")

    @responses.activate
    def test_start_climate_with_temperature(self):
        self.queue("POST", "climate")
        self.check(self.vehicle.start_climate(temperature=20.3),
                action="START", temperature=20.3)

    @responses.activate
    def test_stop_climate(self):
        self.queue("POST", "climate")
        self.check(self.vehicle.stop_climate(), action="STOP")

    @responses.activate
    def test_start_engine(self):
        self.queue("POST", "engine")
        self.check(self.vehicle.start_engine(), action="START")

    @responses.activate
    def test_stop_engine(self):
        self.queue("POST", "engine")
        self.check(self.vehicle.stop_engine(), action="STOP")

    @responses.activate
    def test_turn_engine_on(self):
        self.queue("POST", "engine")
        self.check(self.vehicle.turn_engine_on(), action="ON")

    @responses.activate
    def test_turn_engine_ac1(self):
        self.queue("POST", "engine")
        self.check(self.vehicle.turn_engine_ac1(), action="ACCESSORY_1")

    @responses.activate
    def test_turn_engine_ac2(self):
        self.queue("POST", "engine")
        self.check(self.vehicle.turn_engine_ac2(), action="ACCESSORY_2")

    @responses.activate
    def test_open_hood(self):
        self.queue("POST", "engine/hood")
        self.check(self.vehicle.open_hood(), action="OPEN")

    @responses.activate
    def test_close_hood(self):
        self.queue("POST", "engine/hood")
        self.check(self.vehicle.close_hood(), action="CLOSE")

    @responses.activate
    def test_honk_horn(self):
        self.queue("POST", "horn")
        self.check(self.vehicle.honk_horn(), action="HONK")

    @responses.activate
    def test_flash_headlight(self):
        self.queue("POST", "lights/headlight")
        self.check(self.vehicle.flash_headlight(), action="FLASH")

    @responses.activate
    def test_adjust_mirrors(self):
        self.queue("POST", "mirrors")
        mirrors = [
            {
                "key": "value"
            }
        ]
        self.check(self.vehicle.adjust_mirrors(mirrors), 
                action="TILT", mirrors=mirrors)

    @responses.activate
    def test_start_panic(self):
        self.queue("POST", "panic")
        self.check(self.vehicle.start_panic(), action="START")

    @responses.activate
    def test_stop_panic(self):
        self.queue("POST", "panic")
        self.check(self.vehicle.stop_panic(), action="STOP")

    @responses.activate
    def test_open_charge_port(self):
        self.queue("POST", "ports/charge")
        self.check(self.vehicle.open_charge_port(), action="OPEN")

    @responses.activate
    def test_close_charge_port(self):
        self.queue("POST", "ports/charge")
        self.check(self.vehicle.close_charge_port(), action="CLOSE")

    @responses.activate
    def test_open_fuel_port(self):
        self.queue("POST", "ports/fuel")
        self.check(self.vehicle.open_fuel_port(), action="OPEN")

    @responses.activate
    def test_close_fuel_port(self):
        self.queue("POST", "ports/fuel")
        self.check(self.vehicle.close_fuel_port(), action="CLOSE")

    @responses.activate
    def test_lock(self):
        self.queue("POST", "security")
        self.check(self.vehicle.lock(), action="LOCK")

    @responses.activate
    def test_unlock(self):
        self.queue("POST", "security")
        self.check(self.vehicle.unlock(), action="UNLOCK")

    @responses.activate
    def test_open_sunroof(self):
        self.queue("POST", "sunroof")
        self.check(self.vehicle.open_sunroof(), action="OPEN")

    @responses.activate
    def test_vent_sunroof(self):
        self.queue("POST", "sunroof")
        self.check(self.vehicle.vent_sunroof(), action="VENT")

    @responses.activate
    def test_close_sunroof(self):
        self.queue("POST", "sunroof")
        self.check(self.vehicle.close_sunroof(), action="CLOSE")

    @responses.activate
    def test_open_fronk_trunk(self):
        self.queue("POST", "trunks/front")
        self.check(self.vehicle.open_front_trunk(), action="OPEN")

    @responses.activate
    def test_close_front_trunk(self):
        self.queue("POST", "trunks/front")
        self.check(self.vehicle.close_front_trunk(), action="CLOSE")
        
    @responses.activate
    def test_open_rear_trunk(self):
        self.queue("POST", "trunks/rear")
        self.check(self.vehicle.open_rear_trunk(), action="OPEN")

    @responses.activate
    def test_close_rear_trunk(self):
        self.queue("POST", "trunks/rear")
        self.check(self.vehicle.close_rear_trunk(), action="CLOSE")

    @responses.activate
    def test_open_windows(self):
        self.queue("POST", "windows")
        windows = [ { "key": "value" } ]
        self.check(self.vehicle.open_windows(windows), action="OPEN",
                windows=windows)

    @responses.activate
    def test_close_windows(self):
        self.queue("POST", "windows")
        windows = [ { "key": "value" } ]
        self.check(self.vehicle.close_windows(windows), action="CLOSE",
                windows=windows)

    @responses.activate
    def test_lock_windows(self):
        self.queue("POST", "windows")
        windows = [ { "key": "value" } ]
        self.check(self.vehicle.lock_windows(windows), action="LOCK",
                windows=windows)

    @responses.activate
    def test_unlock_windows(self):
        self.queue("POST", "windows")
        windows = [ { "key": "value" } ]       
        self.check(self.vehicle.unlock_windows(windows), action="UNLOCK",
                windows=windows)
