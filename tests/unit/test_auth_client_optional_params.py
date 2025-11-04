import os
import urllib.parse as urlparse
import tests.auth_helpers as ah
from smartcar import AuthClient


def test_auth_client_without_redirect_uri():
    """Test that AuthClient can be created without a redirect_uri."""
    # Save original environment variables
    original_redirect_uri = os.environ.get("SMARTCAR_REDIRECT_URI")

    try:
        # Remove redirect_uri from environment
        if "SMARTCAR_REDIRECT_URI" in os.environ:
            del os.environ["SMARTCAR_REDIRECT_URI"]

        # Create client without redirect_uri
        client = AuthClient(
            client_id=ah.CLIENT_ID, client_secret=ah.CLIENT_SECRET, mode="test"
        )

        # Should not raise exception
        assert client.redirect_uri is None
    finally:
        # Restore environment variables
        if original_redirect_uri:
            os.environ["SMARTCAR_REDIRECT_URI"] = original_redirect_uri


def test_get_auth_url_without_scope():
    """Test that get_auth_url works without a scope parameter."""
    client = AuthClient(*ah.get_auth_client_params())

    # Call get_auth_url without scope
    test_url = client.get_auth_url()
    query_params = urlparse.parse_qs(test_url)

    # Should include required parameters
    assert query_params["client_id"][0] == ah.CLIENT_ID
    assert query_params["redirect_uri"][0] == ah.REDIRECT_URI
    assert query_params["approval_prompt"][0] == "auto"
    assert "scope" not in query_params

    # With options but no scope
    options = {"state": "test_state"}
    test_url = client.get_auth_url(options=options)
    query_params = urlparse.parse_qs(test_url)

    assert query_params["state"][0] == "test_state"
    assert "scope" not in query_params


def test_auth_url_with_all_optional_params():
    """Test creating an auth URL with all optional parameters."""
    # Create client without redirect_uri
    original_redirect_uri = os.environ.get("SMARTCAR_REDIRECT_URI")

    try:
        # Remove redirect_uri from environment
        if "SMARTCAR_REDIRECT_URI" in os.environ:
            del os.environ["SMARTCAR_REDIRECT_URI"]

        # Create client without redirect_uri
        client = AuthClient(
            client_id=ah.CLIENT_ID, client_secret=ah.CLIENT_SECRET, mode="test"
        )

        # Call get_auth_url without scope or redirect_uri
        test_url = client.get_auth_url()
        query_params = urlparse.parse_qs(test_url)

        # Should include required parameters
        assert query_params["client_id"][0] == ah.CLIENT_ID
        assert "redirect_uri" not in query_params
        assert "scope" not in query_params

    finally:
        # Restore environment variables
        if original_redirect_uri:
            os.environ["SMARTCAR_REDIRECT_URI"] = original_redirect_uri
