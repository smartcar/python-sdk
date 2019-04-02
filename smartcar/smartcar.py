from . import api, const, requester, vehicle
import time
from datetime import datetime, timedelta
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def set_expiration(access):
    expire_date = datetime.utcnow() + timedelta(seconds=access["expires_in"])
    refresh_expire_date = datetime.utcnow() + timedelta(days=60)
    access['expiration'] = expire_date
    access['refresh_expiration'] = refresh_expire_date
    return access

def is_expired(expiration):
    """ Check if an expiration is expired

    Args:
        expiration (datetime): expiration datetime

    Returns:
        bool: true if expired
    """
    return datetime.utcnow() > expiration

def get_vehicle_ids(access_token, limit=10, offset=0):
    """ Get a list of the user's vehicle ids

    Args:
        access_token (str): A valid access token from a previously retrieved
            access object
        limit (integer, optional): The number of vehicle ids to return
        offset (integer, optional): The index to start the vehicle list at

    Returns:
        dict: response containing the list of vehicle ids and paging information

    """
    return api.Api(access_token).vehicles(limit=limit, offset=offset).json()

def get_user_id(access_token):
    """ Retrieve the userId associated with the access_token

    Args:
        access_token (str): Smartcar access token

    Returns:
        str: userId

    """
    return api.Api(access_token).user().json()['id']

class AuthClient(object):

    def __init__(self, client_id, client_secret, redirect_uri, scope=None, test_mode=None, development=None):
        """ A client for accessing the Smartcar API

        Args:
            client_id (str): The application id, provided in the application
                dashboard
            client_secret (str): The application secret, provided in the
                application dashboard
            redirect_uri (str): The URL to redirect to after the user accepts
                or declines the application's permissions. This URL must also be
                present in the Redirect URIs field in the application dashboard
            scope (list, optional): A list of permissions requested by the application
            test_mode (bool, optional): Launch the Smartcar auth flow in test mode. Defaults to false.
                https://smartcar.com/docs#request-authorization
            development (bool, optional): DEPRECATED Launch the Smartcar auth flow in development mode
                to enable mock vehicle brands.

        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth=(client_id, client_secret)
        self.redirect_uri = redirect_uri
        self.scope = scope

        if development:
            import warnings
            message = """Development flag is deprecated. This is discouraged and will be
                         removed in the next major release. Use testMode instead."""
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            self.test_mode = development
        else:
            self.test_mode = test_mode if test_mode else False

    def get_auth_url(self, force=False, state=None, vehicle_info=None):
        """ Generate an OAuth authentication URL

        Args:
            force (bool, optional): Set to True in order to force the approval
                dialog shown to the user. Defaults to False.
            state (bool, optional): A random string that will be passed back on
                redirect, this allows protection against cross-site forgery
                requests. Defaults to None.
            vehicle_info (dict, optional): A dict with a property, make. Allows
                users to bypass the car brand selection screen, allowing the
                user to go directly to the vehicle login screen. 
                Defaults to None. 

        Returns:
            str: authorization url

        """
        base_url = const.CONNECT_URL

        approval_prompt = 'force' if force else 'auto'
        query = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'approval_prompt': approval_prompt,
        }

        if self.test_mode:
            query['mode'] = 'test'

        if self.scope:
            query['scope'] = ' '.join(self.scope)

        if state:
            query['state'] = state
        
        if vehicle_info:
            valid_parameters = ['make']
            for param in valid_parameters:
                if param in vehicle_info:
                    query[param] = vehicle_info[param]

        return base_url + '/oauth/authorize?' + urlencode(query)

    def exchange_code(self, code):
        """ Exchange an authentication code for an access dictionary

        Args:
            code (str): A valid authorization code

        Returns:
            dict: dict containing the access and refresh token

        """
        method = 'POST'
        url = const.AUTH_URL
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
        }
        response = requester.call(method, url, data=data, auth=self.auth).json()
        return set_expiration(response)


    def exchange_refresh_token(self, refresh_token):
        """ Exchange a refresh token for a new access dictionary

        Args:
            refresh_token (str): A valid refresh token from a previously retrieved
                access object

        Returns:
            dict: dict containing access and refresh token

        """
        method = 'POST'
        url = const.AUTH_URL
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = requester.call(method, url, data=data, auth=self.auth).json()
        return set_expiration(response)

    def is_compatible(self, vin, scope):
        """ Determine if a vehicle is compatible with Smartcar

        Args:
            vin (str): the VIN of the vehicle
            scope (list): list of permissions to return compatibility info for

        Returns:
            boolean: true if the vehicle is compatible

        """
        method = 'GET'
        url = const.API_URL + '/compatibility'
        query = {
            'vin': vin,
            'scope': " ".join(scope)
        }
        response = requester.call(method, url, params=query, auth=self.auth).json()
        return response['compatible']
