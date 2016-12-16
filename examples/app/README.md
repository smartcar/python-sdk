# Building an On-Demand Car Cleaning Service With Smartcar

In this quick tutorial we will build a Flask app that uses the Smartcar Python SDK
to set up a simple example service where a user signs up with
their car (or cars), then can press a button on the website to schedule our company
to come clean their car that night. We will get access to their car's location, and the ability
to lock and unlock their car.


## Register your application as a Smartcar Developer

We begin by visiting developer.smartcar.com to create a new application (and register if this is your first time).

We call our application `Flask Demo`, and for now we set one of our Redirect URIs to be `http:localhost:4000/callback`.
You will see the purpose of this redirect URI in just a bit.

You will need your application's __client id__, __client secret__, and __redirect URI__.


## Creating Your Flask App and Installing SDK

Begin by creating a new Flask app. For this example, we will use a very simple structure
with just a main app.py file and a few templates and stylesheets.

Begin by installing `Flask`:

`pip install Flask`

You can create a file called `app.py`, a folder called `static` and an app called `templates`.

Now, to install the Python Smartcar SDK, run the following command:

`pip install smartcar`


## Setting up Smartcar in app.py

We begin by importing `smartcar` along with other needed things at the top of `app.py`, and
initializing a Flask app:

```python
from flask import Flask, request, redirect, render_template
import smartcar   # smartcar sdk
import json

app = Flask(__name__)
```

Now, we will create a new Smartcar client. This is where you will need the __client id__, __client secret__, and __redirect URI__.

Continuing in `app.py`:

```python
client = smartcar.Client(
  client_id='YOUR_APPLICATION_CLIENT_ID'
  client_secret='YOUR_APPLICATION_CLIENT_SECRET'
  redirect_uri='http://localhost:4000/callback',
  scope=['read_vehicle_info', 'read_vin', 'read_security', 'scontrol_security', 'read_location']
)
```

You will notice that we enumerated specific permissions that we will request from the user.
The user will see these exact permissions when they are prompted to authorize your application's
access to the car, and these are the only things you will have access to.

Full documentation on these permissions, and the data you can get with them, can be found
in the API documentation on smartcar.developer.com. For example, looking up `location` in the docs,
we see that we must request the permission `read_location`, and see that the response body
comes with a `latitude` and `longitude` property.

## Using our Smartcar client

### authentication and access codes

In order to use this Smartcar client we have set up, and interact with the user's car(s) in our
application, we must have an access token to provide to the Smartcar client. This will be how
Smartcar knows what user and manufacturer your requests concern. Let's see how to get this.
From the README, the general flow is:

______________________

* Redirect the user to an OEM login page using the URL from `client.get_auth_url(oem)`
* The user will login, and then accept or deny the permissions in your `scope`
    * If the user is already connected to your application, they will not be shown the accept or deny dialog. However the application can force this dialog to be shown with `client.get_auth_url(oem, force=True)`
    * If the user accepts, they will be redirected to your `redirect_uri`. The query field `code` will contain an authentication code. This is *very* important, so save it for later.
    * If the user denies, the query field `code` will equal `"access_denied"`, so you should handle this somehow.

* With your authentication code in hand, use `client.exchange_code(authentication_code)` to exchange your authentication code for an **access object**. This access object will look like this:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "...",
  "created_at": "..."
}
```

* To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**.

____________________

Let us implement this flow in our app.

First, we must send our user to the correct authentication page. Each OEM (car manufacturer) has their
own authentication page, and the url for a specific OEM can be obtained by calling `client.get_auth_url(oem)`.
For example, we will be interacting only with the *Mock* OEM, which all applications automatically
have permission to interact with, and so we call `client.get_auth_url('mock')` to get the auth url we want.

We create a button on the main page that takes users to this url. In our homepage function,
we pass `client_auth_url=client.get_auth_url('mock', force=True)` to our homepage.html template,
and on that template render a button that links to `client_auth_url`.

This takes the user away from
our site to Smartcar's OAuth page, where they will sign in with their account for the 'Mock' OEM.
Remember the callback URI we specified earlier? This is where Smartcar will
redirect back to. We specified 'localhost:4000/callback' as our URI when we created
the client at the top of `app.py`. We also whitelisted this as a URI for our app on smartcar.developer.com, which
is necessary for it to allow redirecting here. So, we place in `app.py`:

```python
@app.route('/callback')
def callback():
  auth_code = request.args.get('code')
  db['access'] = client.exchange_code(auth_code)
  return redirect('/vehicles')
```

This is the exchange part of the flow discussed above. We store in our 'database' the access
object, which is the object that looks like this:

```json
{
  "access_token": "...",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "...",
  "created_at": "..."
}
```

We now have an access token to give the smartcar client!

### Using our access token

We redirect the user to /vehicles in our app, where we will now display for them
all of the vehicles they have authorized our app to access. We first do a
check at this endpoint to make sure there is an access token we can use.

In a full app, we would want a way to map the user to their access token or tokens
(they have a different one for each OEM). However, for our demonstration we just keep
track of it in memory.

If they have one, we check if it is expired, and renew it if so. As found in the SDK readme,
the flow for renewal is:

_______________________

* To make any vehicle data request to the Smartcar API, you'll need to give the SDK a valid **access token**. Access tokens will expire every 2 hours, so you'll need to constantly refresh them. To check if an access object is expired, use `smartcar.expired(access)`.

* It was pretty hard getting that first access token, but from now on it's easy! Calling `client.exchange_token(refresh_token)` will return a new access object using a previous access object's **refresh token**.

______________________

So, in our code we do the following:

```python
@app.route('/vehicles')
def vehicles():
  # ensure that there is an access token
  if not 'access' in db:
    return redirect('/')
  if smartcar.expired(db['access']): # there is a token, but check if it is expired
    db['access'] = client.exchange_token(db['access']['refresh_token']) # use our refresh token to obtain a new access object

```


Once we have confirmed the user has an access token, we can use it to get a list of their vehicles,
and hence interact with these vehicles!

```python
  # get the access token from the access object. We pass this to all smartcar calls
  access_token = db['access']['access_token']
  vehicle_ids = client.get_vehicles(access_token)['vehicles'] # get list of vehicles this user has authorized

  vehicles = []
  for vehicle_id in vehicle_ids:
    vehicles.append(smartcar.Vehicle(vehicle_id, access_token))
```

This gives us an array of vehicle objects. We can call something like `vehicle.location()` to pull
the vehicles latitude and longitude (provided that we included location in our scope of permissions).

And that's it! We use these vehicle objects and obtain data on them, and display them to our user. We
create the button that schedules a clean, but we'll leave the implementation of all of that to a startup!
