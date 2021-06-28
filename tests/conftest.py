import pytest

import smartcar as sc
import smartcar.api as api
import tests.auth_helpers as ah


# Fixtures that can be used throughout the testing suite:

# # Auth Fixtures:
@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def access(client):
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
    access = client.exchange_code(code)
    yield access


# # Vehicle Fixtures:
@pytest.fixture(scope="session")
def chevy_volt(access):
    """
    Using default access token that has the default scope
    permissions (found in ./auth_helpers), return the first
    car. Since the test client defaults to Chevrolet, the first
    car should be a Chevrolet Volt.

    Yields:
        chevy_volt(smartcar.Vehicle)
    """
    vehicle_ids = sc.get_vehicles(access.access_token)
    volt_id = vehicle_ids.vehicles[0]
    return sc.Vehicle(volt_id, access.access_token)


@pytest.fixture(scope="session")
def vw_egolf():
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
    access = client.exchange_code(code)
    vehicle_ids = sc.get_vehicles(access.access_token)
    egolf_id = vehicle_ids.vehicles[0]
    return sc.Vehicle(egolf_id, access.access_token)


# # API Fixture
@pytest.fixture(scope="session")
def api_instance(access, chevy_volt):
    """
    Using the token from the "access" fixture, instantiate a api.Smartcar
    object to play around with. Keep in mind that this class
    is meant to be used frequently.

    Yields: Instance of api.Smartcar
    """
    test_api = api.Smartcar(access.access_token, vehicle_id=chevy_volt.vehicle_id)
    yield test_api
