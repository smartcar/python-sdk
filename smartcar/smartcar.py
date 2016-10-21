from . import const, requester, api, vehicle

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

class Smartcar(object):
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth=(client_id, client_secret)
        self.redirect_uri = redirect_uri
        self.scope = scope
    
    def get_auth_url(self, oem, force=False, state=None):
        """ Get an OEM authorization URL """

        base_url = const.OEMS.get(oem) 
        if not base_url:
            raise ValueError("specified oem is not supported")
        
        approval_prompt = "force" if force else "auto"
        query = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scope),
            "approval_prompt": approval_prompt,
        }
        if state:
            query['state'] = state

        return base_url + '/oauth/authorize?' + urlencode(query)

    def exchange_code(self, code):
        """ Exchange an authentication code for an Access object """
        method = "POST"
        url = const.AUTH_URL
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        return requester.call(method, url, params=params, auth=self.auth)
         

    def exchange_token(self, refresh_token):
        """ Exchange a refresh token for a new Access object """
        method = "POST"
        url = const.AUTH_URL
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        return requester.call(method, url, params=params, auth=self.auth)

    def get_vehicles(self, access_token, limit=10, offset=0):
        """ Get a list of the user's vehicles """
        return api.Api(access_token).vehicles(limit=limit, offset=offset)

    def get_vehicle(self, access_token, vehicle_id):
        """ Get a Vehicle object representing a user's vehicle """
        return vehicle.Vehicle(access_token, vehicle_id)
