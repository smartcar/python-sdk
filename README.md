[![Build Status](https://travis-ci.com/smartcar/python-sdk.svg?token=NkidHDCxcdxrtMy48fzt&branch=master)](https://travis-ci.com/smartcar/python-sdk) [![Coverage Status](https://coveralls.io/repos/github/smartcar/python-sdk/badge.svg?branch=master&t=DF9pBr)](https://coveralls.io/github/smartcar/python-sdk?branch=master)
# Smartcar Python SDK

### Installation

    pip install smartcar

### Running tests

    make test

### Running verbose tests
    
    make test args="--verbose"

### Getting Started

Before you can use this SDK, you need to know your application's **client id**, **client secret**, and **redirect URI**. If you don't have these yet, go to the [smartcar developer](https://developer.smartcar.com) site and create a new application

#### Overall Usage

Now that you have your id, secret and redirect URI, here's a simple overall idea of how to use the SDK to authenticate and make requests with the Smartcar API.

* Create a new smartcar client with `smartcar.Smartcar(client_id, client_secret, redirect_uri, scope)`
* Redirect the user to an OEM login page using the URL from `client.get_auth_url(oem)`
* The user will login, and then accept or deny the permissions in your `scope`
    * If the user is already connected to your application, they will not be shown the accept or deny dialog. However the application can force this dialog to be shown with `client.get_auth_url(oem, force=True)` 
    * If the user accepts, they will be redirected to your `redirect_uri`. The query field `code` will contain an authentication code. This is *very* important, so save it for later.
    * If the user denies, the query field `code` will equal `"access_denied"`, so you should handle this somehow.

* With your authentication code in hand, use `client.exchange_code(authentication_code)` to exchange your authentication code for an **access object**. This access object will look like this:
    ```python
    {
        "access_token": "...",
        "token_type": "Bearer",
        "expires_in": 7200,
        "refresh_token": "...",
        "created_at": "..."
    }
    ```

* To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access tokens will expire every 2 hours, so you'll need to constantly refresh them. To check if an access object is expired, use `client.expired(access)`.

* It was pretty hard getting that first access token, but from now on its easy! Calling `client.exchange_token(refresh_token)` will return a new access object using a previous access object's **refresh token**. This means you can always have a fresh access token, by doing something like this:
    ```python
    def get_fresh_access():
        access = load_access_from_database()
        if smartcar.expired(access):
            new_access = client.exchange_token(access['refresh_token'])
            put_access_into_database(new_access)
            return new_access
        else:
            return access
    
    fresh_access_token = get_fresh_access()['access_token']
    ```
* With your fresh access token in hand, use `client.get_vehicles(access_token)` to get a list of the user's vehicles. The response will look like this:
    ```python
	{
	  "vehicles": [
		"uuid-of-first-vehicle",
		...
		"uuid-of-nth-vehicle"
	  ],
	  "paging": {
		"count": 10,
		"offset": 0
	  }
	}  
    ```
* Now with a **vehicle id** in hand, use `client.get_vehicle(access_token, vehicle_id)` to get a Vehicle object representing the user's vehicle.

* Now you can ask the car to do things, or ask it for some data! For example:

    ```python
    vehicle = client.get_vehicle(access_token, vehicle_id)
    climate_on = vehicle.climate().get('isOn')
    ```
* For a lot more examples on everything you can do with a car, see the [smartcar developer docs](https://developer.smartcar.com/docs)

#### Handling Exceptions

* Any time you make a request to the Smartcar API, something can go wrong. This means that you *really* should wrap each call to `client.exchange_code`, `client.exchange_token`, `client.get_vehicles`, and any vehicle method with some exception handling code. 

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

