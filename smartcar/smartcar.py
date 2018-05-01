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
    access['expiration'] = expire_date.isoformat()
    access['refresh_expiration'] = refresh_expire_date.isoformat()
    return access

def is_expired(expiration):
    """
    Check if an expiration has is expired

    :param expiration: ISO Date format string to check
    """

    return datetime.utcnow().isoformat() > expiration
def get_vehicle_ids(access_token, limit=10, offset=0):
    """
    Get a list of the user's vehicles
    :param access_token: A valid access token from a previously retrieved
        access object
    :param limit: The number of vehicles to return
    :param offset: The index to start the vehicle list at
    """

    return api.Api(access_token).vehicles(limit=limit, offset=offset).json()

def get_user_id(access_token):
    """
    Retrieve the userId associated with the access_token

    :param access_token: Smartcar access token
    :return string containing the userId
    """

    return api.Api(access_token).user().json()['id']

class AuthClient(object):
    """
    A client for accessing the Smartcar API

    :param client_id: The application id, provided in the `application
        dashboard`_

    :param client_secret: The application secret, provided in the `application
        dashboard`_

    :param redirect_uri: The URL to redirect to after the user accepts
        or declines the application's permissions. This URL must also be
        present in the Redirect URIs field in the `application dashboard`_

    :param scope: A list of permissions requested by the application

    .. _application dashboard: https://developer.smartcar.com

    """
    def __init__(self, client_id, client_secret, redirect_uri, scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth=(client_id, client_secret)
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_auth_url(self, force=False, development=False, state=None):
        """
        Generate an OAuth authentication URL

        :param boolean force: Set to True in order to force the approval dialog
            shown to the user

        :param boolean development: Shows the mock OEM for testing, defaults to
            false

        :param str state: A random string that will be passed back on redirect,
            this allows protection against cross-site forgery requests

        :return authorization url
        :rtype str

        """

        base_url = const.CONNECT_URL

        approval_prompt = 'force' if force else 'auto'
        query = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'approval_prompt': approval_prompt,
            'development': development
        }

        if self.scope:
            query['scope'] = ' '.join(self.scope)

        if state:
            query['state'] = state

        return base_url + '/oauth/authorize?' + urlencode(query)

    def exchange_code(self, code):
        """
        Exchange an authentication code for an access object

        :param code: A valid authorization code

        :return dict containing the access and refresh token
        :rtype dict(str, str)

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
        """
        Exchange a refresh token for a new access object

        :param refresh_token: A valid refresh token from a previously retrieved
            access object

        :return dict containing access and refresh token
        :rtype dict(str, str)

        """
        method = 'POST'
        url = const.AUTH_URL
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = requester.call(method, url, data=data, auth=self.auth).json()
        return set_expiration(response)
