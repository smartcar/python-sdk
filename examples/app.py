from flask import Flask, request, redirect
import smartcar
import json

app = Flask(__name__)
client = smartcar.Client(
  client_id='db714877-3755-43bf-9acd-6e14c040802d',
  client_secret='d8a110a7-7525-4964-8da6-b76a8ed20934',
  redirect_uri='http://localhost:4000/callback',
  scope=['read_vehicle_info', 'read_vin', 'read_odometer']
)
db = {}

@app.route('/')
def homepage():
  return """
  <a href="%s"><button>Authorize with Mock</button></a>
  """ % client.get_auth_url('mock', force=True)

@app.route('/callback')
def callback():
  auth_code = request.args.get('code')
  db['access'] = client.exchange_code(auth_code)
  return redirect('/vehicles')

@app.route('/expire')
def expire():
  if not 'access' in db:
    return redirect('/')
  db['access']['expires_in'] = 0;
  return 'expired!'

def get_data(vehicle):
  return {
    'info': vehicle.info(),
    'vin': vehicle.vin(),
    'odometer': vehicle.odometer(),
  }

@app.route('/vehicles')
def vehicles():
  if not 'access' in db:
    return redirect('/')
  if smartcar.expired(db['access']):
    print('expired access, exchaning token')
    print(db['access']['access_token'], db['access']['refresh_token'])
    db['access'] = client.exchange_token(db['access']['refresh_token'])
    print(db['access']['access_token'], db['access']['refresh_token'])

  access_token = db['access']['access_token']
  vehicle_ids = client.get_vehicles(access_token)['vehicles']
  vehicles = [smartcar.Vehicle(vehicle_id, access_token) for vehicle_id in vehicle_ids]
  vehicles[1].set_unit('imperial')
  data = [get_data(vehicle) for vehicle in vehicles]
  return "<pre>" + json.dumps(data, indent=2) + "</pre>"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000, debug=True)
