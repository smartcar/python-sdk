# Smartcar Python Backend SDK [![Build Status][ci-image]][ci-url] [![PyPI version][pypi-image]][pypi-url]

Python package to quickly integrate Smartcar API

## Resources

- [Smartcar Developer Dashboard][smartcar-developer]
- [Smartcar API Reference][smartcar-docs-api]
- [Smartcar Python SDK Reference Documentation][smartcar-python-sdk-reference]

# Installation

```python
# Inside your virtual environment:
pip install smartcar
```

# Usage

## Authentication

Before integrating with Python SDK, you'll need to register an application in
the [Smartcar Developer portal](https://dashboard.smartcar.com). Once you have registered an application, you will have
a Client ID and Client Secret, which will allow you to authorize users.

Now that you have your id, secret and redirect URI, here's a simple overall idea of how to use the SDK to authenticate
and make requests with the Smartcar API.

- In your terminal, export your client id, client secret, and redirect uri as environment variables.

```
export SMARTCAR_CLIENT_ID='<your client id>'
export SMARTCAR_CLIENT_SECRET='<your client secret>'
export SMARTCAR_REDIRECT_URI='<your redirect uri>'
```

- Import the sdk `import smartcar`
- Create a new smartcar `client` with `smartcar.AuthClient()`

```python
import smartcar

client = smartcar.AuthClient()
```

- Redirect the user to an OEM login page using the URL from `client.get_auth_url(scope)`

```python

# Alter this list to specify the scope of permissions your application is requesting access to
scopes = ['read_vehicle_info', 'read_odometer', <scope3>...]

# Generate auth url for User OAuth flow
auth_url = client.get_auth_url(scopes)
```

- The user will login, and then accept or deny the permissions in your `scopes`

  - If the user is already connected to your application, they will not be shown the accept or deny dialog. However
    the application can force this dialog to be shown with `client.get_auth_url(options={"force_prompt"=True})`

- If the user accepts, they will be redirected to your `redirect_uri`. The query field `code` will contain an
  authorization code. This is _very_ important, so save it for later.

  `https://redirect-url.example.com/?code=<AUTHORIZATION_CODE>`

- With your authorization code in hand, use `client.exchange_code(authorization_code)` to exchange your authorization code for an **access object**.

```python
access_object = client.exchange_code(<authorization_code>)
```

This access object will look like this:

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

- To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access
  tokens will expire every 2 hours, so you'll need to constantly refresh them.

- It was pretty hard getting that first access token, but from now on it's easy!
  Calling `client.exchange_refresh_token(refresh_token)` will return a new access object using a previous access
  object's **refresh token**. This means you can always have a fresh access token, by doing something like this:

```python
def get_fresh_access():
    access = load_access_from_database()
    new_access = client.exchange_refresh_token(access['refresh_token'])
    put_access_into_database(new_access)
    
    return new_access


fresh_access_token = get_fresh_access()['access_token']
```

## Vehicle Data and Commands

With your fresh access token in hand, use `smartcar.get_vehicles(access_token)` to get a list of the user's vehicles.

```python
vehicles = smartcar.get_vehicles(<access_token>)

print(vehicles.vehicles)
# [ uuid-of-first-vehicle, "...", uuid-of-nth-vehicle ]

# Vehicle ID of first vehicle
vehicle_id = vehicle.vehicles[0]
```


- Now with a **vehicle id** in hand, use `smartcar.Vehicle(vehicle_id, access_token)` to get a Vehicle object
  representing the user's vehicle.

- Now you can ask the car to do things, or ask it for some data! For example:

```python
vehicle = smartcar.Vehicle(vehicle_id, access_token)

odometer = vehicle.odometer()
print(odometer.distance)

info = vehicle.info()
print(info.make)
print(info.model)

batch = vehicle.batch(paths=['/location'])
location = batch.location()
print(location)
```

- For a lot more examples on everything you can do with a car, see
  the [smartcar developer docs](https://smartcar.com/docs)
- For the full SDK reference guide, visit [REFERENCES.md][smartcar-python-sdk-reference]

## Handling Exceptions

Any time you make a request to the Smartcar API, something can go wrong. This means that you _really_ should wrap each
call to `client.exchange_code`, `client.exchange_refresh_token`, `client.get_vehicles`, and any vehicle method with
some exception handling code.

All exceptions will be of type `smartcar.SmartcarException` with the... exception of missing client
credentials. Navigate below to `AuthClient` for more details.

Upon a vehicle rate limit error, see `SmartcarException.retry_after` (seconds) for when to retry the request.

Check out our [API Reference](https://smartcar.com/docs/api/?version=v2.0#errors)
and [v2.0 Error Guides](https://smartcar.com/docs/errors/v2.0/billing) to learn more.

[ci-url]: https://travis-ci.com/smartcar/python-sdk
[ci-image]: https://travis-ci.com/smartcar/python-sdk.svg?token=FcsopC3DdDmqUpnZsrwg&branch=master
[pypi-url]: https://badge.fury.io/py/smartcar
[pypi-image]: https://badge.fury.io/py/smartcar.svg
[smartcar-developer]: https://developer.smartcar.com
[smartcar-docs-api]: https://smartcar.com/docs
[smartcar-python-sdk-reference]: https://github.com/smartcar/python-sdk/blob/master/REFERENCE.md

# Supported Python Branches

Smartcar aims to support the SDK on all Python branches that have a status of "bugfix" or "security" as defined in the [Python Developer's Guide](https://devguide.python.org/#status-of-python-branches).

In accordance with the Semantic Versioning specification, the addition of support for new Python branches would result in a MINOR version bump and the removal of support for Python branches would result in a MAJOR version bump.
