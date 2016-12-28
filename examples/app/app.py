from flask import Flask, request, redirect, render_template
from flask_bootstrap import Bootstrap
import smartcar
import json

app = Flask(__name__)
Bootstrap(app)

"""
This simple Flask app shows how to use the Smartcar Python SDK to
let users authorize our application to interact with their car(s),
including reading information and location, and unlocking and locking their vehicle.

It begins by importing smartcar, and initializing a client with the SDK. It must provide
the client_id and client_secret obtained from registering the application on developer.smartcar.com.
In addition, it specifies the callback url in your app to redirect to after the user authenticates
with Smartcar, and enumerates the permissions you will ask the user to authorize.
"""

client = smartcar.Client(
  client_id='INSERT YOUR CLIENT ID HERE',
  client_secret='INSERT YOUR CLIENT SECRET HERE',
  redirect_uri='http://localhost:4000/callback',
  scope=['read_vehicle_info', 'read_vin', 'read_security', 'control_security', 'read_location']
)

# dummy database that will hold the user's tokens needed to interact with smartcar.
db = {}
db['vehicles_to_service'] = []

@app.route('/')
def homepage():
  """
  This function uses the smartcar client to get the authentication url for the 'Mock' OEM
  with client.get_auth_url. It renders a page with a button that routes the user to this auth url,
  where they will be prompted to authorize the application to access the permissions enumerated
  in the scope array of our Smartcar initialization.
  """
  return render_template('homepage.html', client_auth_url=client.get_auth_url('mock', force=True))


@app.route('/callback')
def callback():
  """
  In initializing our smartcar instance, we gave it '/callback' as the redirect_uri.
  That means after our user goes to the authentication url and accepts (or rejects)
  the app's permissions, Smartcar will redirect back to our site at '/callback'.
  This function handles the authentication code recieved, and exchanges it for an
  access object. It stores the access object, which we will now use in our
  interactions with the smartcar SDK. We finish by redirecting to '/vehicles'
  """
  auth_code = request.args.get('code')
  db['access'] = client.exchange_code(auth_code)
  return redirect('/vehicles')

def get_data(vehicle):
  """
  get_data takes a vehicle instance and returns an object
  containing its info, vin, and location. It does so by making
  the proper method calls on the object.
  """
  return {
    'info': vehicle.info(),
    'vin': vehicle.vin(),
    'location': vehicle.location()
  }

@app.route('/vehicles')
def vehicles():
  """
  vehicles is called upon visiting /vehicles. It checks that there is an access
  object, and if so checks if it is expired and gets a new one using the refresh_token
  if so.
  The function then calls client.get_vehicles(access_token)['vehicles'] to
  get all vehicles tied to this access token. Note that this will get all of the
  associated user's vehicles of one specific make (in this case 'Mock'). A single user
  may be associated with multiple access objects if they registered multiple
  cars of different makes with our application. We then render a list of these
  vehicles.
  """
  # ensure that there is an access token
  if not 'access' in db:
    return redirect('/')
  if smartcar.expired(db['access']): # there is a token, but check if it is expired
    db['access'] = client.exchange_token(db['access']['refresh_token']) # use our refresh token to obtain a new access object

  # get the access token from the access object. We pass this to all smartcar calls
  access_token = db['access']['access_token']
  vehicle_ids = client.get_vehicles(access_token)['vehicles'] # get list of vehicles this user has authorized

  vehicles = []
  for vehicle_id in vehicle_ids:
    vehicles.append(smartcar.Vehicle(vehicle_id, access_token))

  vehicles[1].set_unit('imperial')
  data = [get_data(vehicle) for vehicle in vehicles]
  # return "<pre>" + json.dumps(data, indent=2) + "</pre>"
  return render_template('vehicles.html', vehicles=data)

@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    """
    user pressed button to schedule a clean for one of their cars, we would handle this
    in a real application. The important things to store are the vehicleId, the access token
    tied to it, and the refresh token in case our access token expires. If we have access to
    these at a later point, then we will be able to continue interacting with the car, i.e,
    in this example we will later want to find and unlock the car to get into it and clean the car.
    """
    vehicleId = request.form['vehicle']
    # store the vehicle id and the codes needed to interact with it through smartcar
    # this will allow you to later interact with the car
    db['vehicles_to_service'].append([(vehicleId, db['access']['access_token'], db['access']['refresh_token'])])
    return redirect('/vehicles')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000, debug=True)
