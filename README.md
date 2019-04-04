# Smartcar Python Backend SDK [![Build Status][ci-image]][ci-url] [![PyPI version][pypi-image]][pypi-url]

## Overview

The [Smartcar API](https://smartcar.com/docs) lets you read vehicle data (location, odometer) and send commands to vehicles (lock, unlock) to connected vehicles using HTTP requests.

To make requests to a vehicle a web or mobile application, the end user must connect their vehicle using [Smartcar's authorization flow](https://smartcar.com/docs/api#authorization).

Before integrating with Python SDK, you'll need to register an application in the [Smartcar Developer portal](https://dashboard.smartcar.com). Once you have registered an application, you will have a Client ID and Client Secret, which will allow you to authorize users.

## Installation
```
pip install smartcar
```

## Overall Usage

Now that you have your id, secret and redirect URI, here's a simple overall idea of how to use the SDK to authenticate and make requests with the Smartcar API.

* Import the sdk `import smartcar`
* Create a new smartcar `client` with `smartcar.AuthClient(client_id, client_secret, redirect_uri, scope, test_mode)`
* Redirect the user to an OEM login page using the URL from `client.get_auth_url()`
* The user will login, and then accept or deny the permissions in your `scope`
    * If the user is already connected to your application, they will not be shown the accept or deny dialog. However the application can force this dialog to be shown with `client.get_auth_url(force=True)`
    * If the user accepts, they will be redirected to your `redirect_uri`. The query field `code` will contain an authentication code. This is *very* important, so save it for later.
    * If the user denies, the query field `code` will equal `"access_denied"`, so you should handle this somehow.

* With your authentication code in hand, use `client.exchange_code(authentication_code)` to exchange your authentication code for an **access object**. This access object will look like this:

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

* To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access tokens will expire every 2 hours, so you'll need to constantly refresh them. To check if an access object is expired, use `smartcar.is_expired(access['expiration'])`.

* It was pretty hard getting that first access token, but from now on it's easy! Calling `client.exchange_refresh_token(refresh_token)` will return a new access object using a previous access object's **refresh token**. This means you can always have a fresh access token, by doing something like this:

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

* With your fresh access token in hand, use `smartcar.get_vehicle_ids(access_token)` to get a list of the user's vehicles. The response will look like this:

```json
{
  "vehicles": [
    "uuid-of-first-vehicle",
    "...",
    "uuid-of-nth-vehicle"
  ],
  "paging": {
    "count": 10,
    "offset": 0
  }
}
```

* Now with a **vehicle id** in hand, use `smartcar.Vehicle(vehicle_id, access_token)` to get a Vehicle object representing the user's vehicle.

* Now you can ask the car to do things, or ask it for some data! For example:

```python
vehicle = smartcar.Vehicle(vehicle_id, access_token)
odometer = vehicle.odometer()['data']['distance']
```

* For a lot more examples on everything you can do with a car, see the [smartcar developer docs](https://smartcar.com/docs)

## Handling Exceptions

* Any time you make a request to the Smartcar API, something can go wrong. This means that you *really* should wrap each call to `client.exchange_code`, `client.exchange_refresh_token`, `client.get_vehicle_ids`, and any vehicle method with some exception handling code.

* Fortunately for you, we've made this as easy as we can! Whenever a request through the SDK returns a non 200 status code, the SDK will throw a nicely named exception for you to handle.

|status code|exception name|
|:-----------:|--------------|
|400|smartcar.ValidationException|
|401|smartcar.AuthenticationException|
|403|smartcar.PermissionException|
|404|smartcar.ResourceNotFoundException|
|409|smartcar.StateException|
|429|smartcar.RateLimitingException|
|430|smartcar.MonthlyLimitExceeded|
|500|smartcar.ServerException|
|501|smartcar.NotCapableException|
|504|smartcar.GatewayTimeoutException|

## AuthClient

### `smartcar.AuthClient(self, client_id, client_secret, redirect_uri, scope=None, test_mode=False)`

A client for accessing the Smartcar API

#### Arguments:
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `client_id`     | String |**Required** Application clientId obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com). |
| `client_secret` | String |**Required** Application clientSecret obtained from [Smartcar Developer Portal](https://dashboard.smartcar.com). |
| `redirect_uri`  | String |**Required** RedirectURI set in [application settings](https://dashboard.smartcar.com/apps). Given URL must match URL in application settings. |
| `scope`         | String[] |**Optional** List of permissions your application requires. This will default to requiring all scopes. The valid permission names are found in the [API Reference](https://smartcar.com/docs/api#get-all-vehicles). |
| `test_mode`   | Boolean |**Optional** Launch the Smartcar auth flow in test mode. |
| `development`   | Boolean |**Optional** DEPRECATED Launch the Smartcar auth flow in development mode to enable mock vehicle brands. |

### `get_auth_url(self, force=False, state=None, vehicle_info=None)`

Generate an OAuth authentication URL

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `force`   | Boolean |**Optional** Setting `forcePrompt` to `true` will show the permissions approval screen on every authentication attempt, even if the user has previously consented to the exact scope of permissions. |
| `state`         | String |**Optional** OAuth state parameter passed to the redirectUri. This parameter may be used for identifying the user who initiated the request. |
| `vehicle_info['make']`  | String |**Optional** Including the dict `vehicle_info` with a `make` property allows users to bypass the car brand selection screen. For a complete list of supported makes, please see our [API Reference](https://smartcar.com/docs/api#authorization) documentation. Makes are case-insensitive. |


#### Return
| Type             | Description         |
|:---------------- |:--------------------|
| String           | Smartcar OAuth authentication URL |

#### Example
```
'https://connect.smartcar.com/oauth/authorize?response_type=token...'
```

### `exchange_code(code)`

Exchange an authentication code for an access dictionary

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `code`         | String |Authorization code to exchange with Smartcar for an `access_token`. |

#### Return
| Type                            | Description         |
|:------------------------------- |:--------------------|
| Dictionary                      | Dictionary containing the access and refresh token |
| Dictionary.`access_token`       | A string representing an access token used to make requests to the Smartcar API. |
| Dictionary.`expiration`         | A datetime of the expiration of the access_token |
| Dictionary.`refresh_token`      | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| Dictionary.`refresh_expiration` | A datetime of the expiration of the refresh_token |
| Dictionary.`token_type`         | Always set to  Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step. |

### `exchange_refresh_token(token)`

Exchange a refresh token for a new access dictionary

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `token`         | String |Refresh token to exchange with Smartcar for an `access_token`. |

#### Return
| Type                            | Description         |
|:------------------------------- |:--------------------|
| Dictionary                      | Dictionary containing the access and refresh token |
| Dictionary.`access_token`       | A string representing an access token used to make requests to the Smartcar API. |
| Dictionary.`expiration`         | A datetime of the expiration of the access_token |
| Dictionary.`refresh_token`      | A string representing a refresh token, which is used to renew access when the current access token expires. The refresh token expires in 60 days. |
| Dictionary.`refresh_expiration` | A datetime of the expiration of the refresh_token |
| Dictionary.`token_type`         | Always set to  Bearer . Token type is used in forming the Authorization header used by the Smartcar API in the following step. |

### `is_compatible(vin, scope)`

Determine vehicle compatibility with Smartcar.

A compatible vehicle is a vehicle that:
1. has the hardware required for internet connectivity,
2. belongs to the makes and models Smartcar supports, and
3. supports the permissions.

_To use this function, please contact us!_

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `vin`         | String |The VIN of the vehicle. |
| `scope`       | String[] | The list of permissions to check compatibility for. Valid permission names are found in the [API Reference](https://smartcar.com/docs/api#get-all-vehicles).

#### Return
| Type                            | Description         |
|:------------------------------- |:--------------------|
| Boolean                         | `False` if the vehicle is NOT compatible. `True` if the vehicle is _likely_ compatible.* |

**\*Note:** as we are only using the VIN, we can only guarantee if a vehicle is NOT compatible with the platform.

## Vehicle

After receiving an `access_token` from the Smartcar Auth flow, your application may make
requests to the vehicle using the `access_token` and the `Vehicle` class.

### `smartcar.Vehicle(self, vehicle_id, access_token, unit_system='metric')`

Initializes a new Vehicle to use for making requests to the Smartcar API.

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---- |:------------- |
| `vehicle_id`    | String | **Required** the vehicle's unique identifier |
| `access_token`  | String | **Required** a valid access token |
| `unit_system`   | String | **Optional** the unit system to use for vehicle data. Defaults to metric. |

### `set_unit_system(self, unit_system)`

Update the unit system to use in requests to the Smartcar API.

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---- |:------------- |
| `unit_system`          | String | the unit system to use (metric/imperial) |

### `permissions(self)`

Returns a paged list of all permissions currently associated with this vehicle.

#### Return
| Type               | Description         |
|:------------------ |:--------------------|
| List[String]       | 	An array of permissions. |

### `info(self)`

Returns a single vehicle object, containing identifying information.

#### Return
| Type               | Description         |
|:------------------ |:--------------------|
| Dictionary         | vehicle's info |
| Dictionary.`id`    | A vehicle ID (UUID v4). |
| Dictionary.`make`  | The manufacturer of the vehicle. |
| Dictionary.`model` | The model of the vehicle. |
| Dictionary.`year`  | The model year. |

### `vin(self)`

Returns the vehicle's manufacturer identifier.

#### Return
| Type               | Description         |
|:------------------ |:--------------------|
| String             | The manufacturer unique identifier. |

### `location(self)`

Returns the location of the vehicle in geographic coordinates.

#### Return
| Type               | Description         |
|:------------------ |:--------------------|
| Dictionary         | vehicle's location  |
| Dictionary.`data`.`latitude`  | The latitude (in degrees). |
| Dictionary.`data`.`longitude` | The longitude (in degrees). |
| Dictionary.`age`   | A datetime for the age of the data |

### `odometer(self)`

Returns the vehicle's current odometer reading.

#### Return
| Type               | Description         |
|:------------------ |:--------------------|
| Dictionary         | vehicle's odometer  |
| Dictionary.`data`.`distance`  | The current odometer of the vehicle |
| Dictionary.`unit_system` | the unit system of the odometer data |
| Dictionary.`age`   | A datetime for the age of the data |

### `disconnect(self)`

Disconnect this vehicle from the connected application.

Note: Calling this method will invalidate your access token and you will
have to have the user reauthorize the vehicle to your application if you
wish to make requests to it

### `unlock(self)`

Unlock the vehicle.

### `lock(self)`

Lock the vehicle.

## Static Methods

### `smartcar.is_expired(expiration)`

Check if an expiration is expired

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---- |:------------- |
| `expiration`    | DateTime | **Required** expiration datetime |

#### Returns

| Type               | Description         |
|:------------------ |:--------------------|
| Boolean            | true if expired     |

### `smartcar.get_vehicle_ids(access_token, limit=10, offset=0)`

Get a list of the user's vehicle ids

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---- |:------------- |
| `access_token`    | String | **Required** A valid access token from a previously retrieved access object |
| `limit`    | Integer | **Optional** The number of vehicle ids to return |
| `offset`    | Integer | **Optional** The index to start the vehicle list at |

#### Returns
| Type               | Description         |
|:------------------ |:--------------------|
| Dictionary            | response containing the list of vehicle ids and paging information  |
| Dictionary.`vehicles` | An array of vehicle IDs. |
| Dictionary.`paging`.`count` | The total number of elements for the entire query (not just the given page). |
| Dictionary.`paging`.`offset` | The current start index of the returned list of elements. |

### `smartcar.get_user_id(access_token)`

 Retrieve the userId associated with the access_token

#### Arguments
| Parameter       | Type | Description   |
|:--------------- |:---- |:------------- |
| `access_token`    | String | **Required** A valid access token from a previously retrieved access object |

#### Returns
| Type               | Description         |
|:------------------ |:--------------------|
| String             | the user id |

[ci-url]: https://travis-ci.com/smartcar/python-sdk
[ci-image]: https://travis-ci.com/smartcar/python-sdk.svg?token=FcsopC3DdDmqUpnZsrwg&branch=master
[pypi-url]: https://badge.fury.io/py/smartcar
[pypi-image]: https://badge.fury.io/py/smartcar.svg
