import os


def validate_env(test_mode: bool = False) -> None:
    """
    Helper Function to determine if environment variables for client id
    and secret are set properly.

    Args:
        test_mode: bool

    Raises:
        Basic Exception
    """
    prefix = "E2E_SMARTCAR" if test_mode else "SMARTCAR"

    if (
            not f"{prefix}_CLIENT_ID" in os.environ
            or not f"{prefix}_CLIENT_SECRET" in os.environ
    ):
        raise Exception(
            f'"{prefix}_CLIENT_ID" and "{prefix}_CLIENT_SECRET" environment variables must be set'
        )
