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

<!-- TODO: File structure -->

Installing Python and Flask will depend on your OS. If you have not installed Flask before,
please see a tutorial like this one https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
before continuing with this.

Now, to install the Python Smartcar SDK, run the following command:

`pip install smartcar`


## Setting up Smartcar in app.py

We begin by importing `smartcar` along with other needed things at the top of `app.py`, and
initializing a Flask app:

```
from flask import Flask, request, redirect, render_template
import smartcar   # smartcar sdk
import json

app = Flask(__name__)
```

Now, we will create a new Smartcar client. This is where you will need the __client id__, __client secret__, and __redirect URI__.

Continuing in `app.py`:

```
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

In order to use this Smartcar client we have set up, and interact with the user's car(s) in our
application, we must have an access token to provide to the Smartcar client. Let's see how to get this.
First, we must send our user to the correct authentication page. Each OEM (car manufacturer) has their
own authentication page, and the url for a specific OEM can be obtained by calling `client.get_auth_url(oem)`.
For example, we will be interacting only with the *Mock* OEM, which all applications automatically
have permission to interact with, and so we call `client.get_auth_url('mock')` to get the auth url we want.

* Button to auth endpoint
* Handle access code
* Get user's vehicles, and access the information we retrieved.
