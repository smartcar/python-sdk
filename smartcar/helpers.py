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
            f'"{prefix}_CLIENT_ID", "{prefix}_CLIENT_SECRET", and '
            f'"{prefix}_CLIENT_REDIRECT_URI environment variables must be set'
        )


def format_flag_query(flags: dict) -> str:
    """
    Takes a dictionary of flags and parses it into a space separated
    string:  "<key>:<value> <key>:<value> ..." to be injected
    as a query parameter.

    Args:
        flags: dict

    Returns:
        str, space separated with "<key>:<value"

        e.g.
        flags == {"flag1 : True, "color" : "green"}
        -> "flag1:True color:green:
    """
    flags_str = ""

    for flag in flags.keys():
        flags_str += f"{flag}:{flags[flag]} "

    return flags_str.strip()
