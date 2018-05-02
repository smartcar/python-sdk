# Smartcar Python SDK [![Build Status][ci-image]][ci-url]

## Overview

The [Smartcar API](https://smartcar.com/docs) lets you read vehicle data (location, odometer) and send commands to vehicles (lock, unlock) to connected vehicles using HTTP requests.

To make requests to a vehicle from a web or mobile application, the end user must connect their vehicle using [Smartcar's authorization flow](https://smartcar.com/docs#authentication). This flow follows the OAuth spec and will return a `code` which can be used to obtain an access token from Smartcar.

The Smartcar Python SDK provides methods to:
1. Generate the link to redirect to for Smartcar's authorization flow.
2. Make a request to Smartcar with the `code` obtained from this authorization flow to obtain an access and refresh token
3. Make requests to the Smartcar API to read vehicle data and send commands to vehicles using the access token obtained in step 2.

Before integrating with Smartcar's SDK, you'll need to register an application in the [Smartcar Developer portal](https://developer.smartcar.com). If you do not have access to the dashboard, please [request access](https://smartcar.com/subscribe).

## Installation
```
pip install smartcar
```

### Running tests
```
make test
```

### Running verbose tests
```
make test args="--verbose"
```

## Overall Usage

Now that you have your id, secret and redirect URI, here's a simple overall idea of how to use the SDK to authenticate and make requests with the Smartcar API.

* Create a new smartcar `client` with `smartcar.AuthClient(client_id, client_secret, redirect_uri, scope, development)`
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
  "created_at": "..."
}
```

* To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access tokens will expire every 2 hours, so you'll need to constantly refresh them. To check if an access object is expired, use `smartcar.expired(access['expiration'])`.

* It was pretty hard getting that first access token, but from now on it's easy! Calling `client.exchange_refresh_token(refresh_token)` will return a new access object using a previous access object's **refresh token**. This means you can always have a fresh access token, by doing something like this:

```python
def get_fresh_access():
    access = load_access_from_database()
    if smartcar.expired(access['expiration']):
        new_access = client.exchange_refresh_token(access['refresh_token'])
        put_access_into_database(new_access)
        return new_access
    else:
        return access

fresh_access_token = get_fresh_access()['access_token']
```

* With your fresh access token in hand, use `client.get_vehicle_ids(access_token)` to get a list of the user's vehicles. The response will look like this:

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
odometer = vehicle.odometer()['data']['odometer']
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

## Authentication Configuration
### `smartcar.AuthClient(self, client_id, client_secret, redirect_uri, scope=None, development=False)`
#### Options:
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `client_id`     | String |**Required** Application clientId obtained from [Smartcar Developer Portal](https://developer.smartcar.com). If you do not have access to the dashboard, please [request access](https://smartcar.com/subscribe). |
| `client_secret` | String |**Required** Application clientSecret obtained from [Smartcar Developer Portal](https://developer.smartcar.com). If you do not have access to the dashboard, please [request access](https://smartcar.com/subscribe). |
| `redirect_uri`  | String |**Required** RedirectURI set in [application settings](https://developer.smartcar.com/apps). Given URL must match URL in application settings. |
| `scope`         | String[] |**Optional** List of permissions your application requires. This will default to requiring all scopes. The valid permission names are found in the [API Reference](https://smartcar.com/docs#get-all-vehicles). |
| `development`   | Boolean |**Optional** Launch Smartcar auth in development mode to enable the mock vehicle brand. |

### `get_auth_url(self, force=False, state=None)`
##### Example
```
'https://connect.smartcar.com/oauth/authorize?response_type=token...'
```

#### Options
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `force`   | Boolean |**Optional** Setting `forcePrompt` to `true` will show the permissions approval screen on every authentication attempt, even if the user has previously consented to the exact scope of permissions. |
| `state`         | String |**Optional** OAuth state parameter passed to the redirectUri. This parameter may be used for identifying the user who initiated the request. |

### `exchange_code(code)`
##### Example
```
'https://connect.smartcar.com/oauth/authorize?response_type=token...'
```

#### Options
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `code`         | String |Authorization code to exchange with Smartcar for an `access_token`. |

### `exchange_refresh_token(token)`
#### Options
| Parameter       | Type | Description   |
|:--------------- |:---|:------------- |
| `token`         | String |Refresh token to exchange with Smartcar for an `access_token`. |

## Make Requests to a Vehicle
After receiving an `access_token` from the Smartcar Auth flow, your application may make
requests to the vehicle using the `access_token` and the `Vehicle` class.


 
-[ci-url]: https://travis-ci.com/smartcar/python-sdk
-[ci-image]: https://travis-ci.com/smartcar/python-sdk.svg?token=FcsopC3DdDmqUpnZsrwg&branch=master
