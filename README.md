# Smartcar Python Backend SDK [![Build Status][ci-image]][ci-url] [![PyPI version][pypi-image]][pypi-url]

## Overview

The [Smartcar API](https://smartcar.com/docs) lets you read vehicle data (location, odometer) and send commands to vehicles (lock, unlock) to connected vehicles using HTTP requests.

To make requests to a vehicle a web or mobile application, the end user must connect their vehicle using [Smartcar Connect](https://smartcar.com/docs/api#authorization).

Before integrating with Python SDK, you'll need to register an application in the [Smartcar Developer portal](https://dashboard.smartcar.com). Once you have registered an application, you will have a Client ID and Client Secret, which will allow you to authorize users.

## Installation
```
pip install smartcar
```

## SDK reference

For detailed documentation on parameters and available methods, please refer to the [SDK reference](doc/).

## Flow

The Python SDK assists with the OAuth authorization process and making requests to the Smartcar API.

1. User clicks "Connect your car" button (or similar button) on your application's front end.
2. User is redirected to the Smartcar authorization flow.
   1. User selects the make of their vehicle.
   2. User is prompted to log in with their vehicle credentials.
   3. User is presented with a set of requested permissions to grant your application.
   4. User can either "Allow" or "Deny" your application's access to the set of permissions.
3. The Smartcar authorization flow redirects the user to a route on your application with the resulting authorization `code`.
4. Your application sends the `client_id`, `client_secret`, and the retrieved authorization `code` to Smartcar in exchange for an `access_token`.
5. Your application uses the `access_token` to make requests to a vehicle.

## Quick Start

### 1. Register a redirect URI

To use the Smartcar authorization flow, you'll need to register an redirect URI. The user will be redirected to the specified URI upon completion of the authorization flow. For web applications, register an HTTP or HTTPS URI. Some example URIs are:

#### Valid:
+ `http://localhost:8000`
+ `https://myapplication.com`

#### Invalid:
+ `http://myapplication.com` (http is only supported for localhost)

You can read more on valid Redirect URIs on the [Smartcar API documentation](https://smartcar.com/docs#redirect-uris).

Once you have constructed your redirect URI, make sure to register it on the [Smartcar dashboard](https://dashboard.smartcar.com).

### 2. Initialize Smartcar

```python
import smartcar

client = smartcar.AuthClient(
  '<your-client-id>',
  '<your-client_secret>',
  '<your-redirect-uri>',
  test_mode=True           # optional
)
```

**Reference:** [`smartcar.AuthClient`](doc#new_Smartcar_new) TODO: UPDATE THIS LINK

### 3. Generate the authorization URL
```python
client.get_auth_url()
```
 TODO: document where this method should be used

**Reference:** [`AuthClient#get_auth_url`](doc#Smartcar+openDialog) TODO: UPDATE THIS LINK

remove the following?
> * The user will login, and then accept or deny the permissions in your `scope`
> * If the user is already connected to your application, they will not be shown the accept or deny dialog. However the application can force this dialog to be shown with `client.get_auth_url(force=True)`

### 4. Exchange the authorization code
```python
access = client.exchange_code('<authorization-code>')
```

**Reference:** [`AuthClient#exchange_code`](doc#Smartcar+openDialog) TODO: UPDATE THIS LINK


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
|501|smartcar.VehicleNotCapableException|
|501|smartcar.SmartcarNotCapableException|
|504|smartcar.GatewayTimeoutException|

Checkout our [Errors documentation][errors] to learn more.

[ci-url]: https://travis-ci.com/smartcar/python-sdk
[ci-image]: https://travis-ci.com/smartcar/python-sdk.svg?token=FcsopC3DdDmqUpnZsrwg&branch=master
[pypi-url]: https://badge.fury.io/py/smartcar
[pypi-image]: https://badge.fury.io/py/smartcar.svg
[errors]: https://smartcar.com/docs/api#errors
