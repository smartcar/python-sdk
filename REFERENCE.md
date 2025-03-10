# AuthClient

### `smartcar.AuthClient(self, client_id, client_secret, redirect_uri, mode='live')`

A client for accessing the Smartcar API

#### Arguments:

| Parameter       | Type   | Required       | Description                                                                                                                       |
| :-------------- | :----- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `client_id`     | String | **Optional**\* | Application clientId obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                   |
| `client_secret` | String | **Optional**\* | Application clientSecret obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                               |
| `redirect_uri`  | String | **Optional**\* | RedirectURI set in [application settings](https://dashboard.smartcar.com/apps). Given URL must match URL in application settings. |
| `mode`          | String | **Optional**   | Determine what mode Smartcar Connect should be launched in. Should be one of test, live or simulated.                             |

##### \***Environment Variables VS Passing Arguments:**

You must EITHER have your client id, secret, and redirect URI exported as environment variables OR passed in as
arguments when instantiating `AuthClient`. It is recommended that you use **environment variables**. These variables
must use the prefix `SMARTCAR_`, in capital snake-case format, like so:

```
export SMARTCAR_CLIENT_ID='<your client id>'
export SMARTCAR_CLIENT_SECRET='<your client secret>'
export SMARTCAR_REDIRECT_URI='<your redirect uri>'
```

AuthClient will use these environment variables by default. If you choose to pass in your client credentials as
arguments, they will take precedence over environment variables.

However, if neither environment variables NOR an argument is passed, an `Exception` will be raised. And the
instantiation of AuthClient will fail.

---

### `get_auth_url(self, force=False, state=None, vehicle_info=None, flags=None)`

Generate Connect URL

#### Arguments

| Parameter               | Type       | Required     | Description                                                                                                                                                                                                                                                                                                     |
| :---------------------- | :--------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scope`                 | String[]   | **Required** | A space-separated list of permissions that your application is requesting access to. Check out [API Reference](https://smartcar.com/docs/api?version=v1.0&language=cURL#permissions) to see available permissions.                                                                                              |
| `options`               | Dictionary | **Optional** | A dictionary where you can pass in additional options as query parameters.                                                                                                                                                                                                                                      |
| `options.force_prompt`  | Boolean    | **Optional** | Setting `forcePrompt` to `true` will show the permissions approval screen on every authentication attempt, even if the user has previously consented to the exact scope of permissions.                                                                                                                         |
| `options.state`         | String     | **Optional** | OAuth state parameter passed to the redirectUri. This parameter may be used for identifying the user who initiated the request.                                                                                                                                                                                 |
| `options.make_bypass`   | String     | **Optional** | Allows users to bypass the car brand selection screen. For a complete list of supported makes, please see our [API Reference](https://smartcar.com/docs/api#authorization) documentation. Makes are case-insensitive.                                                                                           |
| `options.single_select` | Dictionary | **Optional** | Keys of `enabled` (bool) and/or `vin` (string). Sets the behavior of the grant dialog displayed to the user. If `enabled` is set to `true`, `single_select` limits the user to selecting only one vehicle. See the [Single Select guide](https://smartcar.com/docs/guides/single-select/) for more information. |
| `options.flags`         | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to.                                                                                                                                                                                                                                          |
| `options.user`          | String     | **Optional** | An optional developer-defined unique identifier for a vehicle owner. This ID is used to track and aggregate analytics across Connect sessions for each vehicle owner.                                                                                                                                           |


#### Return

| Type   | Description          |
| :----- | :------------------- |
| String | Smartcar Connect URL |
~
#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

#### Example

```
'https://connect.smartcar.com/oauth/authorize?response_type=token...'
```

---

### `exchange_code(code, flags=None)`

Exchange an authorization code for Access named tuple.

#### Arguments

| Parameter      | Type       | Required     | Description                                                                |
| :------------- | :--------- | :----------- | -------------------------------------------------------------------------- |
| `code`         | String     | **Required** | Authorization code to exchange with Smartcar for an `access_token`.        |
| `options`      | Dictionary | **Optional** | A dictionary where you can pass in additional options as query parameters. |
| `opions.flags` | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to.     |

#### Return

| Value                       | Type              | Description                                                                                                                                       |
| :-------------------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Access`                    | typing.NamedTuple | namedtuple containing the access and refresh token                                                                                                |
| `Access.access_token`       | String            | A string representing an access token used to make requests to the Smartcar API.                                                                  |
| `Access.expiration`         | datetime.datetime | A datetime of the expiration of the access_token                                                                                                  |
| `Access.refresh_token`      | String            | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| `Access.refresh_expiration` | datetime.datetime | A datetime of the expiration of the refresh_token                                                                                                 |
| `Access.expires_in`         | Int               | The number of seconds the access token is valid for. This is always set to 7200 (2 hours).                                                        |
| `Access.token_type`         | String            | Always set to Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step.                     |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `exchange_refresh_token(token, flags=None)`

Exchange a refresh token for Access named tuple

#### Arguments

| Parameter      | Type       | Required     | Description                                                                |
| :------------- | :--------- | :----------- | -------------------------------------------------------------------------- |
| `token`        | String     | **Required** | Refresh token to exchange with Smartcar for an `access_token`.             |
| `options`      | Dictionary | **Optional** | A dictionary where you can pass in additional options as query parameters. |
| `opions.flags` | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to.     |

#### Return

| Value                       | Type              | Description                                                                                                                                       |
| :-------------------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Access`                    | typing.NamedTuple | namedtuple containing the access and refresh token                                                                                                |
| `Access.access_token`       | String            | A string representing an access token used to make requests to the Smartcar API.                                                                  |
| `Access.expiration`         | datetime.datetime | A datetime of the expiration of the access_token                                                                                                  |
| `Access.refresh_token`      | String            | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| `Access.refresh_expiration` | datetime.datetime | A datetime of the expiration of the refresh_token                                                                                                 |
| `Access.expires_in`         | Int               | The number of seconds the access token is valid for. This is always set to 7200 (2 hours).                                                        |
| `Access.token_type`         | String            | Always set to Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step.                     |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

# Vehicle

After receiving an `access_token` from the Smartcar Connect, your application may make requests to the vehicle using
the `access_token` and the `Vehicle` class.

---

### `smartcar.Vehicle(self, vehicle_id, access_token, options=None)`

Initializes a new Vehicle to use for making requests to the Smartcar API.

#### Arguments

| Parameter             | Type       | Required     | Description                                                                                              |
| :-------------------- | :--------- | :----------- | :------------------------------------------------------------------------------------------------------- |
| `vehicle_id`          | String     | **Required** | the vehicle's unique identifier                                                                          |
| `access_token`        | String     | **Required** | a valid access token                                                                                     |
| `options`             | Dictionary | **Optional** | a dictionary of optional parameters for vehicle instances                                                |
| `options.unit_system` | String     | **Optional** | the unit system to use for vehicle data. Defaults to metric.                                             |
| `options.version`     | String     | **Optional** | the version of Smartcar API that the instance of the vehicle will send requests to (e.g. '1.0' or '2.0') |

---

### `set_unit_system(self, unit_system)`

Update the unit system to use in requests to the Smartcar API.

#### Arguments

| Parameter     | Type   | Description                              |
| :------------ | :----- | :--------------------------------------- |
| `unit_system` | String | the unit system to use (metric/imperial) |

## Smartcar Vehicle Endpoints

These methods act as wrappers for calls to vehicle-related endpoints to Smartcar API. These methods return explicitly
defined `NamedTuples` from Python's [typing](https://docs.python.org/3/library/typing.html) library. Returned
NamedTuples contain data retrieved upon calling Smartcar API. NamedTuples allow for a rigid return of data with type
hints and dot notation.

```python
# using an instance of Vehicle called "my_model_3"
location = my_model_3.location()
location.latitude
location.longitude
```

---

### `vin(self)`

Returns the vehicle's manufacturer identifier.

#### Return

| Value      | Type                   | Description                                                                |
| :--------- | :--------------------- | :------------------------------------------------------------------------- |
| `Vin`      | typing.NamedTuple      | The returned object with vin-related data                                  |
| `Vin.vin`  | String                 | The manufacturer unique identifier.                                        |
| `Vin.meta` | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `charge(self)`

Returns the vehicle's charging status of an electric vehicle.

#### Return

| Value                  | Type                   | Description                                                                                             |
| :--------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------ |
| `Charge`               | typing.NamedTuple      | The returned object with charging status data                                                           |
| `Charge.is_plugged_in` | Boolean                | State of whether car is plugged in                                                                      |
| `Charge.status`        | String                 | Indicates the current state of the charge system. Can be `FULLY_CHARGED`, `CHARGING`, or `NOT_CHARGING` |
| `Charge.meta`          | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                              |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `battery(self)`

Returns the vehicle's battery status.

#### Return

| Value                       | Type                   | Description                                                                                                                                                                      |
| :-------------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Battery`                   | typing.NamedTuple      | The returned object with battery status data                                                                                                                                     |
| `Battery.percent_remaining` | Float                  | The remaining level of charge in the battery (in percent)                                                                                                                        |
| `Battery.range`             | Float                  | The estimated remaining distance the car can travel (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Battery.meta`              | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                                                       |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `battery_capacity(self)`

Returns the total capacity of an electric vehicle's battery.

#### Return

| Value                      | Type                   | Description                                                                |
| :------------------------- | :--------------------- | :------------------------------------------------------------------------- |
| `BatteryCapacity`          | typing.NamedTuple      | The returned object data regarding total capacity of an EV's battery       |
| `BatteryCapacity.capacity` | Float                  | vehicle's battery capacity in kWh                                          |
| `BatteryCapacity.meta`     | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `nominal_capacity(self)`

Returns a list of nominal rated battery capacities for a vehicle.


#### Return

| Value                                 | Type                       | Description                                                                                               |
| :------------------------------------ | :------------------------- | :-------------------------------------------------------------------------------------------------------- |
| `NominalCapacity`                     | typing.NamedTuple          | The returned object data regarding the nominal rated battery capacities for a vehicle                     |
| `NominalCapacity.availableCapacities` | List[AvailableCapacity]    | A list of the rated nominal capacities available for a vehicle                                            |
| `NominalCapacity.capacity`            | Optional[SelectedCapacity] | The rated nominal capacity for the vehicle's battery in kWh                                               |
| `NominalCapacity.url`                 | Optional[String]           | A URL that will launch the flow for a vehicle owner to specify the correct battery capacity for a vehicle |
| `NominalCapacity.meta`                | collections.namedtuple     | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                |


Each AvailableCapacity entry contains:
- `capacity` (float): The rated nominal capacity for the vehicle's battery in kWh
- `description` (String, optional): A a description of the uniquness for the nominal capacity and engine type 

Each SelectedCapacity entry contains:
- `capacity` (float): The rated nominal capacity for the vehicle's battery kWh 
- `source` (String): Indicates if this capacity was determined by a user or Smartcar

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `fuel(self)`

Returns the vehicle's fuel status.

#### Return

| Value                    | Type                   | Description                                                                                                                                                                      |
| :----------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Fuel`                   | typing.NamedTuple      | The returned object with vehicle's fuel status                                                                                                                                   |
| `Fuel.range`             | Float                  | The estimated remaining distance the car can travel (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Fuel.percent_remaining` | Float                  | The remaining level of fuel in the tank (in percent)                                                                                                                             |
| `Fuel.amount_remaining`  | Float                  | The amount of fuel in the tank (in liters or gallons (US)). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).            |
| `Fuel.meta`              | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                                                       |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `tire_pressure(self)`

Returns the vehicle's tire pressure status.

#### Return

| Value                      | Type                   | Description                                                                                                                                                                 |
| :------------------------- | :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TirePressure`             | typing.NamedTuple      | The returned object with vehicle's tire pressure status                                                                                                                     |
| `TirePressure.front_left`  | Float                  | The current air pressure of the front left tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).  |
| `TirePressure.front_right` | Float                  | The current air pressure of the front right tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `TirePressure.back_left`   | Float                  | The current air pressure of the back left tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).   |
| `TirePressure.back_right`  | Float                  | The current air pressure of the back right tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).  |
| `TirePressure.meta`        | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                                                  |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `engine_oil(self)`

Returns the vehicle's oil status.

#### Return

| Value                      | Type                   | Description                                                                                                  |
| :------------------------- | :--------------------- | :----------------------------------------------------------------------------------------------------------- |
| `EngineOil`                | typing.NamedTuple      | The returned object with vehicle's oil status                                                                |
| `EngineOil.life_remaining` | Float                  | The engine oil's remaining life span (as a percentage). Oil life is based on the current quality of the oil. |
| `EngineOil.meta`           | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                   |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `odometer(self)`

Returns the vehicle's current odometer reading.

#### Return

| Value               | Type                   | Description                                                                                                                                                              |
| :------------------ | :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Odometer`          | typing.NamedTuple      | The returned object with vehicle's odometer (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Odometer.distance` | Float                  | The current odometer of the vehicle                                                                                                                                      |
| `Odometer.meta`     | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                                               |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `location(self)`

Returns the location of the vehicle in geographic coordinates.

#### Return

| Value                | Type                   | Description                                                                |
| :------------------- | :--------------------- | :------------------------------------------------------------------------- |
| `Location`           | typing.NamedTuple      | The returned object with vehicle's location/coordinates                    |
| `Location.latitude`  | Float                  | The latitude (in degrees).                                                 |
| `Location.longitude` | Float                  | The longitude (in degrees).                                                |
| `Location.meta`      | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `service_history(self, start_date: Optional[str] = None, end_date: Optional[str] = None)`

Returns a list of all the service records performed on the vehicle, filtered by the optional date range. If no dates are specified, records from the last year are returned.

#### Args

| Argument     | Type          | Description                                                                                 |
| :----------- | :------------ | :------------------------------------------------------------------------------------------ |
| `start_date` | Optional[str] | The start date for the record filter, in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.SSSZ' format. |
| `end_date`   | Optional[str] | The end date for the record filter, similar format to start_date.                           |

#### Return

| Value                  | Type                   | Description                                                                |
| :--------------------- | :--------------------- | :------------------------------------------------------------------------- |
| `ServiceHistory`       | typing.NamedTuple      | The returned object with a list of service entries.                        |
| `ServiceHistory.items` | List[ServiceRecord]    | List of service records describing maintenance activities.                 |
| `ServiceHistory.meta`  | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

`SmartcarException` - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `diagnostic_system_status(self)`

Retrieve the status of various diagnostic systems in the vehicle.

#### Return

| Value                         | Type                   | Description                                                          |
| :---------------------------- | :--------------------- | :------------------------------------------------------------------- |
| `DiagnosticSystemStatus`      | typing.NamedTuple      | The returned object with diagnostic system statuses data             |
| `DiagnosticSystemStatus.systems` | List[Dict]         | List of system statuses, each with `system_id`, `status`, and `description` |
| `DiagnosticSystemStatus.meta` | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

Each system entry contains:
- `system_id` (String): Unique identifier for the system.
- `status` (String): Status of the system, either "OK" or "ALERT".
- `description` (String, optional): Additional context or description for the status, if any.

---

### `diagnostic_trouble_codes(self)`

Retrieve active diagnostic trouble codes (DTCs) for the vehicle.

#### Return

| Value                      | Type                   | Description                                              |
| :------------------------- | :--------------------- | :------------------------------------------------------- |
| `DiagnosticTroubleCodes`   | typing.NamedTuple      | The returned object with active diagnostic trouble codes  |
| `DiagnosticTroubleCodes.active_codes` | List[Dict]     | List of active DTCs, each with `code` and `timestamp`    |
| `DiagnosticTroubleCodes.meta` | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

Each trouble code entry contains:
- `code` (String): The DTC code representing the issue.
- `timestamp` (String, optional): ISO 8601 timestamp when the code was triggered. May be `null` if unavailable.

---
### `attributes(self)`

Returns a single vehicle object, containing identifying information.

#### Return

| Value              | Type                   | Description                                                                |
| :----------------- | :--------------------- | :------------------------------------------------------------------------- |
| `Attributes`       | typing.NamedTuple      | The returned object with vehicle's info                                    |
| `Attributes.id`    | String                 | A vehicle ID (UUID v4).                                                    |
| `Attributes.make`  | String                 | The manufacturer of the vehicle.                                           |
| `Attributes.model` | String                 | The model of the vehicle.                                                  |
| `Attributes.year`  | String                 | The model year.                                                            |
| `Attributes.meta`  | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `lock(self)`

Lock the vehicle.

#### Return

| Value            | Type                   | Description                                                                         |
| :--------------- | :--------------------- | :---------------------------------------------------------------------------------- |
| `Action`         | typing.NamedTuple      | The returned object with vehicle's status after sending a request to lock the doors |
| `Action.status`  | String                 | Set to "success" on successful request.                                             |
| `Action.message` | String                 | Message of the response.                                                            |
| `Action.meta`    | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)          |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `unlock(self)`

Unlock the vehicle.

#### Return

| Value            | Type                   | Description                                                                           |
| :--------------- | :--------------------- | :------------------------------------------------------------------------------------ |
| `Action`         | typing.NamedTuple      | The returned object with vehicle's status after sending a request to unlock the doors |
| `Action.status`  | String                 | Set to "success" on successful request.                                               |
| `Action.message` | String                 | Message of the response.                                                              |
| `Action.meta`    | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)            |

#### Raises

<code>SmartcarException</code> on unsuccessful request

---

### `start_charge(self)`

Start charging the vehicle.

#### Return

| Value            | Type                   | Description                                                                                |
| :--------------- | :--------------------- | :----------------------------------------------------------------------------------------- |
| `Action`         | typing.NamedTuple      | The returned object with vehicle's status after sending a request to start charging the EV |
| `Action.status`  | String                 | Set to "success" on successful request.                                                    |
| `Action.message` | String                 | Message of the response.                                                                   |
| `Action.meta`    | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                 |

#### Raises

<code>SmartcarException</code> on unsuccessful request

---

### `send_destination(self, latitude, longitude)`

Send destination to the vehicle.

#### Arguments

| Name        | Type  | Description                   |
| :---------- | :---- | :---------------------------- |
| `latitude`  | Float | Latitude of the destination.  |
| `longitude` | Float | Longitude of the destination. |


#### Return

| Value            | Type              | Description                                                    |
| :--------------- | :---------------- | :------------------------------------------------------------- |
| `Action`         | typing.NamedTuple | The returned object after sending a destination to the vehicle |
| `Action.status`  | String            | Set to "success" on successful request.                        |
| `Action.message` | String            | Message of the response.                                       |

#### Raises

<code>SmartcarException</code> on unsuccessful request

---

### `stop_charge(self)`

Stop charging the vehicle.

#### Return

| Value            | Type                   | Description                                                                               |
| :--------------- | :--------------------- | :---------------------------------------------------------------------------------------- |
| `Action`         | typing.NamedTuple      | The returned object with vehicle's status after sending a request to stop charging the EV |
| `Action.status`  | String                 | Set to "success" on successful request.                                                   |
| `Action.message` | String                 | Message of the response.                                                                  |
| `Action.meta`    | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                |

#### Raises

<code>SmartcarException</code> on unsuccessful request

---

### `permissions(self)`

Returns the `Permissions` NamedTuple, paged list of all permissions currently associated with this vehicle.

#### Return

| Value                     | Type                   | Description                                                                |
| :------------------------ | :--------------------- | :------------------------------------------------------------------------- |
| `Permissions`             | typing.NamedTuple      | The returned object with the vehicle's permissions                         |
| `Permissions.unit_system` | String[]               | An array of permission                                                     |
| `Permissions.meta`        | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

---

### `lock_status(self)`

Returns the lock status for a vehicle and the open status of its doors, windows, storage units, sunroof and charging port where available. The open status array(s) will be empty if a vehicle has partial support. The request will error if lock status can not be retrieved from the vehicle or the brand is not supported.

#### Return

| Value             | Type                   | Description                                                                                                                                                                                      |
| :---------------- | :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `isLocked`        | bool                   | Indicates whether the vehicle is locked.                                                                                                                                                         |
| `doors`           | typing.NamedTuple      | An array of the open status of the vehicle's doors. Array length will vary depending on the number of doors.                                                                                     |
| `windows`         | typing.NamedTuple      | An array of the open status of the vehicle's windows. Array length will vary depending on the number of windows.                                                                                 |
| `sunroof`         | typing.NamedTuple      | An array of the open status of the vehicle's sunroofs.                                                                                                                                           |
| `storage`         | typing.NamedTuple      | An array of the open status of the vehicle's storages. For internal combustion and plug-in hybrid vehicles, front refers to the engine hood. For battery vehicles, this will be the front trunk. |
| `chargingPort`    | typing.NamedTuple      | An array of the open status of the vehicle's charging port                                                                                                                                       |
| `LockStatus.meta` | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                                                                       |


---

### `batch(self, paths)`

Make a batch request to the vehicle. WARNING: This feature is exclusive to [Smartcar Pro](https://smartcar.com/pricing/)
members. Visit https://smartcar.com/pricing to sign up and gain access.

The batch method will return a named tuple named `batch`. Methods are attached to `batch`, and they return
a `NamedTuple` corresponding to the path requested. Upon erroneous requests, the method will throw a `SmartcarException`
.

#### Arguments

| Parameter | Type | Description                                                |
| :-------- | :--- | :--------------------------------------------------------- |
| `paths`   | List | A list of paths (i.e. `"/odometer"`) to request data from. |

#### Return

| Value             | Type                   | Description                                                                                                |
| :---------------- | :--------------------- | :--------------------------------------------------------------------------------------------------------- |
| `Batch`           | collections.namedtuple | The returned object with the results of the requests. Each request results in the corresponding NamedTuple |
| `Batch.<request>` | lambda                 | Returns the appropriate NamedTuple for the request. e.g. `Batch.odometer` -> <Odometer>                    |
| `Batch.meta`      | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                 |

#### Example Response

```Python
# Sending a batch request for vehicle attributes (i.e. '/'), odometer, and engine oil
batch = my_tesla_3.batch(['/', '/odometer', '/engine/oil'])

# attributes (path: "/")
batch.attributes()  # returns Attributes(...) or raises SmartcarException

# Get 'make' of the car
batch.attributes().make

# odometer (path: "/odometer")
batch.odometer()  # returns Odometer(...) or raises SmartcarException

# odometer (path: "/engine/oil")
batch.engine_oil()  # returns EngineOil(...) or raises SmartcarException

```

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `disconnect(self)`

Disconnect this vehicle from the connected application.

#### Returns

| Value           | Type                   | Description                                                                       |
| :-------------- | :--------------------- | :-------------------------------------------------------------------------------- |
| `Status`        | typing.NamedTuple      | The returned object with vehicle's "status" after sending a request to disconnect |
| `Status.status` | String                 | Set to "success" on successful request.                                           |
| `Status.meta`   | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)        |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

Note: Calling this method will invalidate your access token, and you will have to have the user reauthorize the vehicle
to your application if you wish to make requests to it

---

### `subscribe(self, webhook_id)`

Subscribe vehicle to a Smartcar webhook.

#### Arguments

| Parameter    | Type   | Description                                             |
| :----------- | :----- | :------------------------------------------------------ |
| `webhook_id` | String | Id of the webhook you want to subscribe your vehicle to |

#### Returns

| Value                  | Type                   | Description                                                                                   |
| :--------------------- | :--------------------- | :-------------------------------------------------------------------------------------------- |
| `Subscribe`            | typing.NamedTuple      | The returned object with vehicle's "status" after sending a request to subscribe to a webhook |
| `Subscribe.webhook_id` | String                 | Id of requested webhook                                                                       |
| `Subscribe.vehicle_id` | String                 | Id of requested vehicle                                                                       |
| `Subscribe.meta`       | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                    |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `unsubscribe(self, amt, webhook_id)`

Unsubscribe vehicle from a Smartcar webhook.

#### Arguments

| Parameter    | Type   | Description                                                 |
| :----------- | :----- | :---------------------------------------------------------- |
| `webhook_id` | String | Id of the webhook you want to unsubscribe your vehicle from |

#### Returns

| Value           | Type                   | Description                                                                                       |
| :-------------- | :--------------------- | :------------------------------------------------------------------------------------------------ |
| `Status`        | typing.NamedTuple      | The returned object with vehicle's "status" after sending a request to unsubscribe from a webhook |
| `Status.status` | String                 | Set to "success" on successful request.                                                           |
| `Status.meta`   | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                        |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

# Static Methods

### `smartcar.set_api_version(version)`

Sets the version of Smartcar API to use

#### Arguments

| Parameter | Type   | Description                     |
| :-------- | :----- | :------------------------------ |
| `version` | String | version number (example: "2.0") |

#### Returns

| Type |
| :--- |
| None |

---

### `smartcar.get_vehicles(access_token, limit=10, offset=0)`

Get a list of the user's vehicle ids

#### Arguments

| Parameter       | Type       | Required     | Description                                                      |
| :-------------- | :--------- | :----------- | :--------------------------------------------------------------- |
| `access_token`  | String     | **Required** | A valid access token from a previously retrieved access object   |
| `paging`        | Dictionary | **Optional** | An optional dictionary to implement paging for returned vehicles |
| `paging.limit`  | Integer    | **Optional** | The number of vehicle ids to return                              |
| `paging.offset` | Integer    | **Optional** | The index to start the vehicle list at                           |

#### Returns

| Value                    | Type                   | Description                                                                |
| :----------------------- | :--------------------- | :------------------------------------------------------------------------- |
| `Vehicles`               | typing.NamedTuple      | The returned object with the list of vehicle ids and paging information    |
| `Vehicles.vehicles`      | String                 | Set to "success" on successful request.                                    |
| `Vehicles.paging`        | typing.NamedTuple      | Contains paging information of returned data                               |
| `Vehicles.paging.limit`  | Integer                | The number of vehicle ids to return                                        |
| `Vehicles.paging.offset` | Integer                | The index to start the vehicle list at                                     |
| `Vehicles.meta`          | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `smartcar.get_user_id(access_token)`

Retrieve the userId associated with the access_token

#### Arguments

| Parameter      | Type   | Description                                                    |
| :------------- | :----- | :------------------------------------------------------------- |
| `access_token` | String | A valid access token from a previously retrieved access object |

#### Returns

| Value       | Type                   | Description                                                                |
| :---------- | :--------------------- | :------------------------------------------------------------------------- |
| `User`      | typing.NamedTuple      | The returned object with User id                                           |
| `User.id`   | String                 | The user id                                                                |
| `User.meta` | collections.namedtuple | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`) |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

---

### `get_compatibility(vin, scope, country='US', options=None)`

Determine vehicle compatibility with Smartcar.

A compatible vehicle is a vehicle that:

1. has the hardware required for internet connectivity,
2. belongs to the makes and models Smartcar supports, and
3. supports the permissions.

#### Arguments

| Parameter               | Type       | Required     | Description                                                                                                                                                  |
| :---------------------- | :--------- | :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vin`                   | String     | **Required** | The VIN of the vehicle.                                                                                                                                      |
| `scope`                 | String[]   | **Required** | The list of permissions to check compatibility for. Valid permission names are found in the [API Reference](https://smartcar.com/docs/api#get-all-vehicles). |
| `country`               | String     | **Optional** | For details on how to specify country code strings refer to [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).                          |
| `options`               | Dictionary | **Optional** | A dictionary where you can pass in additional options as query parameters.                                                                                   |
| `options.client_id`     | String     | **Optional** | Application clientId obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                                              |
| `options.client_secret` | String     | **Optional** | Application clientSecret obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                                          |
| `options.version`       | String     | **Optional** | the version of Smartcar API (e.g. '1.0' or '2.0')                                                                                                            |
| `options.flags`         | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to.                                                                                       |

#### Return

| Value                                     | Type                   | Availability          | Description                                                                                                                                         |
| :---------------------------------------- | :--------------------- | :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Compatibility`                           | typing.NamedTuple      | **API v1.0 and v2.0** | The returned object with vehicle's compatibility with the permissions (scope) checked                                                               |
| `Compatibility.compatible`                | Boolean                | **API v1.0 and v2.0** | Whether the vehicle is compatible with the permissions                                                                                              |
| `Compatibility.reason`                    | String or None         | **API v2.0 only**     | One of the following string values if compatible is false, null otherwise: "VEHICLE_NOT_COMPATIBLE", "MAKE_NOT_COMPATIBLE"                          |
| `Compatibility.capabilities`              | List                   | **API v2.0 only**     | A list containing the set of endpoints that the provided scope value can provide authorization for. This list will be empty if compatible is false. |
| `Compatibility.capabilities[].permission` | String                 | **API v2.0 only**     | One of the permissions provided in the scope parameter.                                                                                             |
| `Compatibility.capabilities[].endpoint`   | String                 | **API v2.0 only**     | One of the endpoints that the permission authorizes access to.                                                                                      |
| `Compatibility.capabilities[].capable`    | Boolean                | **API v2.0 only**     | True if the vehicle is likely capable of this feature, False otherwise.                                                                             |
| `Compatibility.capabilities[].reason`     | String or None         | **API v2.0 only**     | One of the following string values if compatible is false, null otherwise: "VEHICLE_NOT_COMPATIBLE", "SMARTCAR_NOT_CAPABLE"                         |
| `Compatibility.meta`                      | collections.namedtuple | **API v1.0 and v2.0** | Smartcar response headers (`request_id`, `data_age`, `fetched_at`, and/or `unit_system`)                                                                          |

#### Raises

<code>SmartcarException</code> - See
the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

**\*Note:** as we are only using the VIN, we can only guarantee if a vehicle is NOT compatible with the platform.

# Webhook Static Methods

### `hash_challenge(amt, challenge)`

Take the random string received in the challenge request and use your Application Management Token (amt) to create an
SHA-256 based HMAC. Return the hex-encoding of the resulting hash

#### Arguments

| Parameter   | Type   | Required     | Description                                                              |
| :---------- | :----- | :----------- | :----------------------------------------------------------------------- |
| `amt`       | String | **Required** | Application Management Token (found in Smartcar dashboard).              |
| `challenge` | String | **Required** | The randomly generated string received after sending a challenge request |

#### Return

| Type   | Description                    |
| :----- | :----------------------------- |
| String | Hex-encoding of resulting hash |

---

### `verify_payload(amt, signature, body)`

Verify webhook payload against AMT and signature.

#### Arguments

| Parameter   | Type   | Required     | Description                                                 |
| :---------- | :----- | :----------- | :---------------------------------------------------------- |
| `amt`       | String | **Required** | Application Management Token (found in Smartcar dashboard). |
| `signature` | String | **Required** | sc-signature header value                                   |
| `body`      | String | **Required** | Stringified JSON of the webhook response body               |

#### Return

| Type    | Description                            |
| :------ | :------------------------------------- |
| Boolean | Matching signature and response header |

# Vehicle Management Static Methods

### `get_connections(amt, filter, paging)`

Get a paged list of all the vehicles that are connected to the application associated with the management API token used
sorted in descending order by connection date.

#### Arguments

| Parameter           | Type       | Required     | Description                                                              |
| :------------------ | :--------- | :----------- | :----------------------------------------------------------------------- |
| `amt`               | String     | **Required** | Application Management Token (found in Smartcar dashboard).              |
| `filter`            | Dictionary | **Optional** | The randomly generated string received after sending a challenge request |
| `filter.user_id`    | String     | **Optional** | The randomly generated string received after sending a challenge request |
| `filter.vehicle_id` | String     | **Optional** | The randomly generated string received after sending a challenge request |
| `paging`            | String     | **Optional** | The randomly generated string received after sending a challenge request |
| `paging.cursor`     | Integer    | **Optional** | The randomly generated string received after sending a challenge request |
| `paging.limit`      | String     | **Optional** | The randomly generated string received after sending a challenge request |

#### Return

| Value                                       | Type              | Availability          | Description |
| :------------------------------------------ | :---------------- | :-------------------- | :---------- |
| `GetConnections`                            | typing.NamedTuple | **API v1.0 and v2.0** |             |
| `GetConnections.connections`                | Boolean           | **API v1.0 and v2.0** |             |
| `GetConnections.connections[].user_id`      | Boolean           | **API v1.0 and v2.0** |             |
| `GetConnections.connections[].vehicle_id`   | Boolean           | **API v1.0 and v2.0** |             |
| `GetConnections.connections[].connected_at` | Boolean           | **API v1.0 and v2.0** |             |
| `Compatibility.paging`                      | String or None    | **API v1.0 and v2.0** |             |
| `Compatibility.paging.cursor`               | List              | **API v1.0 and v2.0** |             |

### `delete_connections(amt, filter)`

Delete all the connections by vehicle or user ID and returns a list of all connections that were deleted.

#### Arguments

| Parameter           | Type       | Required     | Description                                                              |
| :------------------ | :--------- | :----------- | :----------------------------------------------------------------------- |
| `amt`               | String     | **Required** | Application Management Token (found in Smartcar dashboard).              |
| `filter`            | Dictionary | **Optional** | The randomly generated string received after sending a challenge request |
| `filter.user_id`    | String     | **Optional** | The randomly generated string received after sending a challenge request |
| `filter.vehicle_id` | String     | **Optional** | The randomly generated string received after sending a challenge request |

#### Return

| Value                                     | Type              | Availability          | Description |
| :---------------------------------------- | :---------------- | :-------------------- | :---------- |
| `GetConnections`                          | typing.NamedTuple | **API v1.0 and v2.0** |             |
| `GetConnections.connections`              | Boolean           | **API v1.0 and v2.0** |             |
| `GetConnections.connections[].user_id`    | Boolean           | **API v1.0 and v2.0** |             |
| `GetConnections.connections[].vehicle_id` | Boolean           | **API v1.0 and v2.0** |             |
