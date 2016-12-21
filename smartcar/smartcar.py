from . import const, requester, api, vehicle
import time
from datetime import datetime, timedelta
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def set_expiration(access):
    expire_date = datetime.utcnow() + timedelta(seconds=access["expires_in"])
    access["expiration"] = expire_date.isoformat()
    return access

def expired(expiration):
    """
    Check if an access object's access token is expired
    :param access: access object to check
    """
    return datetime.utcnow().isoformat() > expiration

class Client(object):
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
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth=(client_id, client_secret)
        self.redirect_uri = redirect_uri
        self.scope = scope

    def get_auth_url(self, oem, force=False, state=None):
        """
        Generate an OAuth authentication URL for the specified OEM

        :param str oem: The name of an oem

        :param boolean force: Set to True in order to force the approval dialog
            shown to the user

        :param str state: A random string that will be passed back on redirect,
            this allows protection against cross-site forgery requests

        """

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
        """
        Exchange an authentication code for an access object

        :param code: A valid authorization code

        """
        method = "POST"
        url = const.AUTH_URL
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = requester.call(method, url, data=data, auth=self.auth)
        return set_expiration(response)


    def exchange_token(self, refresh_token):
        """
        Exchange a refresh token for a new access object

        :param refresh_token: A valid refresh token from a previously retrieved
            access object

        """
        method = "POST"
        url = const.AUTH_URL
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        response = requester.call(method, url, data=data, auth=self.auth)
        return set_expiration(response)

    def get_vehicles(self, access_token, limit=10, offset=0):
        """
        Get a list of the user's vehicles

        :param access_token: A valid access token from a previously retrieved
            access object

        :param limit: The number of vehicles to return

        :param offset: The index to start the vehicle list at

        """
        return api.Api(access_token).vehicles(limit=limit, offset=offset)
