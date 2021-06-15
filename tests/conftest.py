import pytest

import smartcar as sc
import tests.auth_helpers as ah


# Fixtures that can be used throughout the testing suite:

# # Auth Fixtures:
@pytest.fixture(scope="module")
def client():
    """
    Set up a Smartcar Auth Client with test parameters.
    Default test parameters include default scope of permissions,
    which matches that of Chevrolet. Default test brand for this
    client will be Chevrolet.

    Yields:
        client(smartcar.AuthClient)
        A smartcar auth client that can be used across all tests.
    """
    client = sc.AuthClient(*ah.get_auth_client_params())
    yield client


@pytest.fixture(scope="module")
def access_object(client):
    """
    Using the client fixture, go through Smartcar connect auth
    flow and acquire an access object. This object will have
    access and refresh tokens that can be used throughout the
    project.

    Yields:
        access_object(dict)
    """
    auth_url = client.get_auth_url(scope=ah.DEFAULT_SCOPE)
    code = ah.run_auth_flow(auth_url)
    access_object = client.exchange_code(code)
    yield access_object


# # Vehicle Fixtures:
@pytest.fixture(scope="module")
def chevy_volt(access_object):
    """
    Using default access token that has the default scope
    permissions (found in ./auth_helpers), return the first
    car. Since the test client defaults to Chevrolet, the first
    car should be a Chevrolet Volt.

    Yields:
        chevy_volt(smartcar.Vehicle)
    """
    access_token = access_object["access_token"]
    vehicle_ids = sc.get_vehicles(access_token)
    volt_id = vehicle_ids["vehicles"][0]
    return sc.Vehicle(volt_id, access_token)


@pytest.fixture(scope="module")
def vw_egolf(access_object):
    """
    Using a separate instance of smartcar.AuthClient,
    run the Smartcar connect auth flow with different scope of permissions and
    a different brand. This time, get the first vehicle acquired for Volkswagen.
    The first car should be a Volkswagen E-Golf.

    Yields:
        vw_egolf(smartcar.Vehicle)
    """
    client = sc.AuthClient(*ah.get_auth_client_params())
    code = ah.run_auth_flow(
        client.get_auth_url(["required:control_charge"]), "VOLKSWAGEN"
    )
    access_token = client.exchange_code(code)["access_token"]
    vehicle_ids = sc.get_vehicles(access_token)
    egolf_id = vehicle_ids["vehicles"][0]
    return sc.Vehicle(egolf_id, access_token)
