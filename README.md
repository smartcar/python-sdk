# Smartcar Python Backend SDK [![Build Status][ci-image]][ci-url] [![PyPI version][pypi-image]][pypi-url]

# Overview

The [Smartcar API](https://smartcar.com/docs) lets you read vehicle data (e.g. location, odometer) and send commands to vehicles (e.g. lock, unlock) to connected vehicles using HTTP requests.

To make requests to a vehicle a web or mobile application, the end user must connect their vehicle using [Smartcar Connect](https://smartcar.com/docs/api#authorization).

Before integrating with Python SDK, you'll need to register an application in the [Smartcar Developer portal](https://dashboard.smartcar.com). Once you have registered an application, you will have a Client ID and Client Secret, which will allow you to authorize users.

# Supported Versions
Python 3.7, 3.8, or 3.9

# Installation

```
pip install smartcar
```

# Overall Usage

Now that you have your id, secret and redirect URI, here's a simple overall idea of how to use the SDK to authenticate and make requests with the Smartcar API.

- In your terminal, export your client id, client secret, and redirect uri as environment variables.

```
export SMARTCAR_CLIENT_ID='<your client id>'
export SMARTCAR_CLIENT_ID='<your client secret>'
export SMARTCAR_CLIENT_ID='<your redirect URI>'
```

- Import the sdk `import smartcar`
- Create a new smartcar `client` with `smartcar.AuthClient()`
- Redirect the user to an OEM login page using the URL from `client.get_auth_url()`
- The user will login, and then accept or deny the permissions in your `scope`

  - If the user is already connected to your application, they will not be shown the accept or deny dialog. However the application can force this dialog to be shown with `client.get_auth_url(force=True)`
  - If the user accepts, they will be redirected to your `redirect_uri`. The query field `code` will contain an authorization code. This is _very_ important, so save it for later.
  - If the user denies, the query field `code` will equal `"access_denied"`, so you should handle this somehow.

- With your authorization code in hand, use `client.exchange_code(authorization_code)` to exchange your authorization code for an **access object**. This access object will look like this:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expiration": "2018-05-02T18:04:25+00:00",
  "refresh_token": "...",
  "refresh_expiration": "2018-06-02T18:03:25+00:00",
  "expires_in": "..."
}
```

- To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access tokens will expire every 2 hours, so you'll need to constantly refresh them. To check if an access object is expired, use `smartcar.is_expired(access['expiration'])`.

- It was pretty hard getting that first access token, but from now on it's easy! Calling `client.exchange_refresh_token(refresh_token)` will return a new access object using a previous access object's **refresh token**. This means you can always have a fresh access token, by doing something like this:

```python
def get_fresh_access():
    access = load_access_from_database()
    if smartcar.is_expired(access['expiration']):
        new_access = client.exchange_refresh_token(access['refresh_token'])
        put_access_into_database(new_access)
        return new_access
    else:
        return access

fresh_access_token = get_fresh_access()['access_token']
```

- With your fresh access token in hand, use `smartcar.get_vehicle_ids(access_token)` to get a list of the user's vehicles. The response will look like this:

```json
{
  "vehicles": ["uuid-of-first-vehicle", "...", "uuid-of-nth-vehicle"],
  "paging": {
    "count": 10,
    "offset": 0
  }
}
```

- Now with a **vehicle id** in hand, use `smartcar.Vehicle(vehicle_id, access_token)` to get a Vehicle object representing the user's vehicle.

- Now you can ask the car to do things, or ask it for some data! For example:

```python
vehicle = smartcar.Vehicle(vehicle_id, access_token)
odometer = vehicle.odometer().distance
```

- For a lot more examples on everything you can do with a car, see the [smartcar developer docs](https://smartcar.com/docs)

# Handling Exceptions

Any time you make a request to the Smartcar API, something can go wrong. This means that you _really_ should wrap each call to `client.exchange_code`, `client.exchange_refresh_token`, `client.get_vehicle_ids`, and any vehicle method with some exception handling code.

All exceptions will be of type `smartcar.SmartcarException` with the... exception (sorry, not sorry) of missing client credentials. Navigate below to `AuthClient` for more details.

Check out our [API Reference](https://smartcar.com/docs/api/?version=v2.0#errors) and [v2.0 Error Guides](https://smartcar.com/docs/errors/v2.0/billing) to learn more.

# AuthClient

### `smartcar.AuthClient(self, client_id, client_secret, redirect_uri, test_mode=False)`

A client for accessing the Smartcar API

#### Arguments:

| Parameter       | Type    | Required       | Description                                                                                                                       |
| :-------------- | :------ | :------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `client_id`     | String  | **Optional\*** | Application clientId obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                   |
| `client_secret` | String  | **Optional\*** | Application clientSecret obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                               |
| `redirect_uri`  | String  | **Optional\*** | RedirectURI set in [application settings](https://dashboard.smartcar.com/apps). Given URL must match URL in application settings. |
| `test_mode`     | Boolean | **Optional**   | Launch the Smartcar Connect in test mode.                                                                                         |

##### \***Environment Variables VS Passing Arguments:**

You must EITHER have your client id, secret, and redirect URI exported as environment variables OR passed in as arguments when instantiating `AuthClient`. It is recommended that you use **environment variables**. These variables must use the prefix `SMARTCAR_`, in capital snake-case format, like so:

```
export SMARTCAR_CLIENT_ID='<your client id>'
export SMARTCAR_CLIENT_SECRET='<your client secret>'
export SMARTCAR_REDIRECT_URI='<your redirect uri>'
```

AuthClient will use these environment variables by default. However, if you choose to pass in your client credientials as arguments, they will take precedence over environment variables.

However, if neither environment variables NOR an argument is passed, an `Exception` will be raised. And the instantiation of AuthClient will fail.

### `get_auth_url(self, force=False, state=None, vehicle_info=None, flags=None)`

Generate the Connect URL

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

#### Return

| Type   | Description          |
| :----- | :------------------- |
| String | Smartcar Connect URL |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

#### Example

```
'https://connect.smartcar.com/oauth/authorize?response_type=token...'
```

### `exchange_code(code, flags=None)`

Exchange an authorization code for an access dictionary

#### Arguments

| Parameter | Type       | Required     | Description                                                            |
| :-------- | :--------- | :----------- | ---------------------------------------------------------------------- |
| `code`    | String     | **Required** | Authorization code to exchange with Smartcar for an `access_token`.    |
| `flags`   | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to. |

#### Return

| Type                            | Description                                                                                                                                       |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dictionary                      | Dictionary containing the access and refresh token                                                                                                |
| Dictionary.`access_token`       | A string representing an access token used to make requests to the Smartcar API.                                                                  |
| Dictionary.`expiration`         | A datetime of the expiration of the access_token                                                                                                  |
| Dictionary.`refresh_token`      | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| Dictionary.`refresh_expiration` | A datetime of the expiration of the refresh_token                                                                                                 |
| Dictionary.`token_type`         | Always set to Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step.                     |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `exchange_refresh_token(token, flags=None)`

Exchange a refresh token for a new access dictionary

#### Arguments

| Parameter | Type       | Required     | Description                                                            |
| :-------- | :--------- | :----------- | ---------------------------------------------------------------------- |
| `token`   | String     | **Required** | Refresh token to exchange with Smartcar for an `access_token`.         |
| `flags`   | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to. |

#### Return

| Type                            | Description                                                                                                                                       |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dictionary                      | Dictionary containing the access and refresh token                                                                                                |
| Dictionary.`access_token`       | A string representing an access token used to make requests to the Smartcar API.                                                                  |
| Dictionary.`expiration`         | A datetime of the expiration of the access_token                                                                                                  |
| Dictionary.`refresh_token`      | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| Dictionary.`refresh_expiration` | A datetime of the expiration of the refresh_token                                                                                                 |
| Dictionary.`token_type`         | Always set to Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step.                     |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

# Vehicle

After receiving an `access_token` from the Smartcar Connect, your application may make
requests to the vehicle using the `access_token` and the `Vehicle` class.

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

### `set_unit_system(self, unit_system)`

Update the unit system to use in requests to the Smartcar API.

#### Arguments

| Parameter     | Type   | Description                              |
| :------------ | :----- | :--------------------------------------- |
| `unit_system` | String | the unit system to use (metric/imperial) |

### Smartcar Vehicle Endpoints

These methods act as wrappers for calls to vehicle-related endpoints to Smartcar API. These methods return explicitly defined `NamedTuples` from Python's [typing](https://docs.python.org/3/library/typing.html) library. Returned NamedTuples contain data retrieved upon calling Smartcar API. NamedTuples allow for a rigid return of data with type hints and dot notation.

```python
# using an instance of Vehicle called "my_model_3"
location = my_model_3.location()
print location.latitude
print location.longitude
```

### Meta

All NamedTuples returned as a result from using a `Vehicle` method includes a `meta` attribute. The `Meta` class generates an object with attribute names and values matching the keys and values of a dictionary. `Meta` can contain a variable amount of attributes. Each attribute in any `Meta` object represents a response header and various information about the request in lowercase, snake-case format.

e.g. If a call to Smartcar API resulted with a response header of `"SC-unit-type" : "metric"`, the `Meta` object will contain an attribute of `sc_unit_type`.

```python
# Using the above example:
print location.meta
print location.meta.request_id
```

### `vin(self)`

Returns the vehicle's manufacturer identifier.

#### Return

| Value      | Type       | Description                                                              |
| :--------- | :--------- | :----------------------------------------------------------------------- |
| `Vin`      | NamedTuple | The returned object with vin-related data                                |
| `Vin.vin`  | String     | The manufacturer unique identifier.                                      |
| `Vin.meta` | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `charge(self)`

Returns the vehicle's charging status of an electric vehicle.

#### Return

| Value                  | Type       | Description                                                                                             |
| :--------------------- | :--------- | :------------------------------------------------------------------------------------------------------ |
| `Charge`               | NamedTuple | The returned object with charging status data                                                           |
| `Charge.is_plugged_in` | Boolean    | State of whether car is plugged in                                                                      |
| `Charge.status`        | String     | Indicates the current state of the charge system. Can be `FULLY_CHARGED`, `CHARGING`, or `NOT_CHARGING` |
| `Charge.meta`          | Meta       | Response headers and other information about the response of the request                                |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `battery(self)`

Returns the vehicle's battery status.

#### Return

| Value                       | Type       | Description                                                                                                                                                                      |
| :-------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Battery`                   | NamedTuple | The returned object with battery status data                                                                                                                                     |
| `Battery.percent_remaining` | Float      | The remaining level of charge in the battery (in percent)                                                                                                                        |
| `Battery.range`             | Float      | The estimated remaining distance the car can travel (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Battery.meta`              | Meta       | Response headers and other information about the response of the request                                                                                                         |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `battery_capacity(self)`

Returns the total capacity of an electric vehicle's battery. Please [contact us](mailto:hello@smartcar.com) to request early access.

#### Return

| Value                      | Type       | Description                                                              |
| :------------------------- | :--------- | :----------------------------------------------------------------------- |
| `BatteryCapacity`          | NamedTuple | The returned object data regarding total capacity of an EV's battery     |
| `BatteryCapacity.capacity` | Float      | vehicle's battery capacity in kWh                                        |
| `BatteryCapacity.meta`     | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `fuel(self)`

Returns the vehicle's fuel status.

#### Return

| Value                    | Type       | Description                                                                                                                                                                      |
| :----------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Fuel`                   | NamedTuple | The returned object with vehicle's fuel status                                                                                                                                   |
| `Fuel.range`             | Float      | The estimated remaining distance the car can travel (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Fuel.percent_remaining` | Float      | The remaining level of fuel in the tank (in percent)                                                                                                                             |
| `Fuel.amount_remaining`  | Float      | The amount of fuel in the tank (in liters or gallons (US)). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).            |
| `Fuel.meta`              | Meta       | Response headers and other information about the response of the request                                                                                                         |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `tire_pressure(self)`

Returns the vehicle's tire pressure status.

#### Return

| Value                      | Type       | Description                                                                                                                                                                 |
| :------------------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TirePressure`             | NamedTuple | The returned object with vehicle's tire pressure status                                                                                                                     |
| `TirePressure.front_left`  | Float      | The current air pressure of the front left tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).  |
| `TirePressure.front_right` | Float      | The current air pressure of the front right tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `TirePressure.back_left`   | Float      | The current air pressure of the back left tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).   |
| `TirePressure.back_right`  | Float      | The current air pressure of the back right tire (in psi or kpa). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system).  |
| `TirePressure.meta`        | Meta       | Response headers and other information about the response of the request                                                                                                    |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `oil(self)`

Returns the vehicle's oil status.

#### Return

| Value                | Type       | Description                                                                                                  |
| :------------------- | :--------- | :----------------------------------------------------------------------------------------------------------- |
| `Oil`                | NamedTuple | The returned object with vehicle's oil status                                                                |
| `Oil.life_remaining` | Float      | The engine oil's remaining life span (as a percentage). Oil life is based on the current quality of the oil. |
| `Oil.meta`           | Meta       | Response headers and other information about the response of the request                                     |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `odometer(self)`

Returns the vehicle's current odometer reading.

#### Return

| Value               | Type       | Description                                                                                                                                                              |
| :------------------ | :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Odometer`          | NamedTuple | The returned object with vehicle's odometer (in kms or miles). To set unit, see [setUnitSystem](https://github.com/smartcar/python-sdk#set_unit_systemself-unit_system). |
| `Odometer.distance` | Float      | The current odometer of the vehicle                                                                                                                                      |
| `Odometer.meta`     | Meta       | Response headers and other information about the response of the request                                                                                                 |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `location(self)`

Returns the location of the vehicle in geographic coordinates.

#### Return

| Value                | Type       | Description                                                              |
| :------------------- | :--------- | :----------------------------------------------------------------------- |
| `Location`           | NamedTuple | The returned object with vehicle's location/coordinates                  |
| `Location.latitude`  | Float      | The latitude (in degrees).                                               |
| `Location.longitude` | Float      | The longitude (in degrees).                                              |
| `Location.meta`      | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `info(self)`

Returns a single vehicle object, containing identifying information.

#### Return

| Value        | Type       | Description                                                              |
| :----------- | :--------- | :----------------------------------------------------------------------- |
| `Info`       | NamedTuple | The returned object with vehicle's info                                  |
| `Info.id`    | String     | A vehicle ID (UUID v4).                                                  |
| `Info.make`  | String     | The manufacturer of the vehicle.                                         |
| `Info.model` | String     | The model of the vehicle.                                                |
| `Info.year`  | String     | The model year.                                                          |
| `Info.meta`  | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `lock(self)`

Lock the vehicle.

#### Return

| Value           | Type       | Description                                                                           |
| :-------------- | :--------- | :------------------------------------------------------------------------------------ |
| `Status`        | NamedTuple | The returned object with vehicle's "status" after sending a request to lock the doors |
| `Status.status` | String     | Set to "success" on successful request.                                               |
| `Status.meta`   | Meta       | Response headers and other information about the response of the request              |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `unlock(self)`

Unlock the vehicle.

#### Return

| Value           | Type       | Description                                                                             |
| :-------------- | :--------- | :-------------------------------------------------------------------------------------- |
| `Status`        | NamedTuple | The returned object with vehicle's "status" after sending a request to unlock the doors |
| `Status.status` | String     | Set to "success" on successful request.                                                 |
| `Status.meta`   | Meta       | Response headers and other information about the response of the request                |

#### Raises

<code>SmartcarException</code> on unsuccessful request

### `start_charge(self)`

Start charging the vehicle.

#### Return

| Value           | Type       | Description                                                                                  |
| :-------------- | :--------- | :------------------------------------------------------------------------------------------- |
| `Status`        | NamedTuple | The returned object with vehicle's "status" after sending a request to start charging the EV |
| `Status.status` | String     | Set to "success" on successful request.                                                      |
| `Status.meta`   | Meta       | Response headers and other information about the response of the request                     |

#### Raises

<code>SmartcarException</code> on unsuccessful request

### `stop_charge(self)`

Stop charging the vehicle.

#### Return

| Value           | Type       | Description                                                                                 |
| :-------------- | :--------- | :------------------------------------------------------------------------------------------ |
| `Status`        | NamedTuple | The returned object with vehicle's "status" after sending a request to stop charging the EV |
| `Status.status` | String     | Set to "success" on successful request.                                                     |
| `Status.meta`   | Meta       | Response headers and other information about the response of the request                    |

#### Raises

<code>SmartcarException</code> on unsuccessful request

### `permissions(self)`

Returns the `Permissions` NamedTuple, paged list of all permissions currently associated with this vehicle.

#### Return

| Value                     | Type       | Description                                                              |
| :------------------------ | :--------- | :----------------------------------------------------------------------- |
| `Permissions`             | NamedTuple | The returned object with the vehicle's permissions                       |
| `Permissions.unit_system` | String[]   | An array of permission                                                   |
| `Permissions.meta`        | Meta       | Response headers and other information about the response of the request |

### `batch(self, paths)`

Make a batch request to the vehicle. WARNING: This feature is exclusive to [Smartcar Pro](https://smartcar.com/pricing/) members. Visit https://smartcar.com/pricing to sign up and gain access.

#### Arguments

| Parameter | Type | Description                                                |
| :-------- | :--- | :--------------------------------------------------------- |
| `paths`   | List | A list of paths (i.e. `"/odometer"`) to request data from. |

#### Return

| Value             | Type       | Description                                                                                                |
| :---------------- | :--------- | :--------------------------------------------------------------------------------------------------------- |
| `Batch`           | Batch      | The returned object with the results of the requests. Each request results in the corresponding NamedTuple |
| `Batch.<request>` | NamedTuple | The appropriate NamedTuple for the request. e.g. `Batch.odometer` -> <Odometer>                            |
| `Batch.meta`      | Meta       | Response headers and other information about the response of the request                                   |

#### Example Response

```Python
# Upon sending a batch request to '/odometer' and '/location' for an instantiated Vehicle "my_tesla_3"

batch = my_tesla_3.batch(['/odometer', '/location'])

print batch.odometer.distance
print batch.location.longitude
print batch.meta
```

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `disconnect(self)`

Disconnect this vehicle from the connected application.

#### Returns

| Value           | Type       | Description                                                                       |
| :-------------- | :--------- | :-------------------------------------------------------------------------------- |
| `Status`        | NamedTuple | The returned object with vehicle's "status" after sending a request to disconnect |
| `Status.status` | String     | Set to "success" on successful request.                                           |
| `Status.meta`   | Meta       | Response headers and other information about the response of the request          |

#### Raises

<code>SmartcarException</code> - on unsuccessful request. See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

Note: Calling this method will invalidate your access token and you will
have to have the user reauthorize the vehicle to your application if you
wish to make requests to it

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

### `smartcar.is_expired(expiration)`

Check if an expiration is expired

#### Arguments

| Parameter    | Type     | Description         |
| :----------- | :------- | :------------------ |
| `expiration` | DateTime | expiration datetime |

#### Returns

| Type    | Description     |
| :------ | :-------------- |
| Boolean | true if expired |

### `smartcar.get_vehicle_ids(access_token, limit=10, offset=0)`

Get a list of the user's vehicle ids

#### Arguments

| Parameter       | Type       | Required     | Description                                                      |
| :-------------- | :--------- | :----------- | :--------------------------------------------------------------- |
| `access_token`  | String     | **Required** | A valid access token from a previously retrieved access object   |
| `paging`        | Dictionary | **Optional** | An optional dictionary to implement paging for returned vehicles |
| `paging.limit`  | Integer    | **Optional** | The number of vehicle ids to return                              |
| `paging.offset` | Integer    | **Optional** | The index to start the vehicle list at                           |

#### Returns

| Value                    | Type       | Description                                                              |
| :----------------------- | :--------- | :----------------------------------------------------------------------- |
| `Vehicles`               | NamedTuple | The returned object with the list of vehicle ids and paging information  |
| `Vehicles.vehicles`      | String     | Set to "success" on successful request.                                  |
| `Vehicles.paging`        | NamedTuple | Contains paging information of returned data                             |
| `Vehicles.paging.limit`  | Integer    | The number of vehicle ids to return                                      |
| `Vehicles.paging.offset` | Integer    | The index to start the vehicle list at                                   |
| `Vehicles.meta`          | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

### `smartcar.get_user_id(access_token)`

Retrieve the userId associated with the access_token

#### Arguments

| Parameter      | Type   | Description                                                    |
| :------------- | :----- | :------------------------------------------------------------- |
| `access_token` | String | A valid access token from a previously retrieved access object |

#### Returns

| Value       | Type       | Description                                                              |
| :---------- | :--------- | :----------------------------------------------------------------------- |
| `User`      | NamedTuple | The returned object with User id                                         |
| `User.id`   | String     | The user id                                                              |
| `User.meta` | Meta       | Response headers and other information about the response of the request |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

[ci-url]: https://travis-ci.com/smartcar/python-sdk
[ci-image]: https://travis-ci.com/smartcar/python-sdk.svg?token=FcsopC3DdDmqUpnZsrwg&branch=master
[pypi-url]: https://badge.fury.io/py/smartcar
[pypi-image]: https://badge.fury.io/py/smartcar.svg

### `get_compatibility(vin, scope, country='US', options=None)`

Determine vehicle compatibility with Smartcar.

A compatible vehicle is a vehicle that:

1. has the hardware required for internet connectivity,
2. belongs to the makes and models Smartcar supports, and
3. supports the permissions.

_To use this function, please contact us!_

#### Arguments

| Parameter               | Type       | Required     | Description                                                                                                                                                  |
| :---------------------- | :--------- | :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vin`                   | String     | **Required** | The VIN of the vehicle.                                                                                                                                      |
| `scope`                 | String[]   | **Required** | The list of permissions to check compatibility for. Valid permission names are found in the [API Reference](https://smartcar.com/docs/api#get-all-vehicles). |
| `country`               | String     | **Optional** | For details on how to specify country code strings refer to [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).                          |
| `options`               | Dictionary | **Optional** | A dictionary where you can pass in additional options as query parameters.                                                                                   |
| `options.client_id`     | String     | **Optional** | Application clientId obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                                              |
| `options.client_secret` | String     | **Optional** | Application clientSecret obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com).                                                          |
| `options.flags`         | Dictionary | **Optional** | Dictionary of feature flags that your application has early access to.                                                                                       |

#### Return

| Value                      | Type       | Description                                                                           |
| :------------------------- | :--------- | :------------------------------------------------------------------------------------ |
| `Compatibility`            | NamedTuple | The returned object with vehicle's compatibility with the permissions (scope) checked |
| `Compatibility.compatible` | Boolean    | Whether the vehicle is compatibile with the permissions (or not)                      |
| `Compatibility.meta`       | Meta       | Response headers and other information about the response of the request              |

#### Raises

<code>SmartcarException</code> - See the [exceptions section](https://github.com/smartcar/python-sdk#handling-exceptions) for all possible exceptions.

**\*Note:** as we are only using the VIN, we can only guarantee if a vehicle is NOT compatible with the platform.
