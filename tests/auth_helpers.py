import os
import uuid
import logging
import urllib.parse as urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

import smartcar.helpers as helpers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Verify all E2E variables are present ('E2E_<CLIENT VARIABLE>')
helpers.validate_env(mode="test")

# Smartcar client environment variables (Required)
CLIENT_ID = os.environ["E2E_SMARTCAR_CLIENT_ID"]
CLIENT_SECRET = os.environ["E2E_SMARTCAR_CLIENT_SECRET"]
BROWSER = os.environ.get("BROWSER", "firefox")
REDIRECT_URI = "https://example.com/auth"

# Variables for testing webhooks (Optional):
APPLICATION_MANAGEMENT_TOKEN = os.environ.get("E2E_SMARTCAR_AMT")
WEBHOOK_ID = os.environ.get("E2E_SMARTCAR_WEBHOOK_ID")


# Helper function for boolean environment variables
def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1';
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """
    return str(val).lower() in ("y", "yes", "t", "true", "on", "1")


# Variables for Geckodriver
HEADLESS = "CI" in os.environ or (
    "HEADLESS" in os.environ and strtobool(os.environ["HEADLESS"])
)

# A list of all available permissions on Smartcar API
DEFAULT_SCOPE = [
    "required:read_vehicle_info",
    "required:read_location",
    "required:read_odometer",
    "required:control_security",
    "required:read_vin",
    "required:read_fuel",
    "required:read_battery",
    "read_charge",
    "required:read_engine_oil",
    "required:read_tires",
    "required:read_security",
]


def get_auth_client_params() -> list:
    """Get the parameters needed to initialize a Smartcar auth client.

    Returns:
        list: [client_id, client_secret, redirect_uri, test_mode, mode]
    """
    mode = "test"
    return [CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, True, mode]


def get_code_from_url(url: str) -> str:
    """Extract the authorization code from a callback URL.

    Args:
        url: The callback URL containing the authorization code

    Returns:
        str: The authorization code

    Raises:
        ValueError: If the code is not found in the URL
    """
    search_params = urlparse.parse_qs(urlparse.urlparse(url).query)

    if "code" not in search_params:
        error_msg = search_params.get("error", ["Unknown error"])[0]
        raise ValueError(f"Authorization code not found in URL. Error: {error_msg}")

    return search_params["code"][0]  # Return first code if multiple exist


def get_driver(browser_name, headless=False):
    if browser_name.lower() == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.headless = headless
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name.lower() == "firefox":
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service
        import os
        import subprocess
        import logging

        logger = logging.getLogger(__name__)

        # Create Firefox options
        options = Options()

        # Set Firefox binary location to our local installation
        firefox_path = os.path.expanduser('~/firefox-latest-smartcar/firefox/firefox')
        if not os.path.exists(firefox_path):
            raise FileNotFoundError(
                f"Firefox not found at {firefox_path}. "
                "Please run the setup script first."
            )

        options.binary_location = firefox_path

        # Basic Firefox configuration
        options.set_preference("browser.shell.checkDefaultBrowser", False)
        options.set_preference("browser.startup.homepage_override.mstone", "ignore")
        options.set_preference("browser.startup.page", 0)
        options.set_preference("browser.sessionstore.resume_from_crash", False)
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)
        options.add_argument('--no-remote')

        # Set up Firefox service with logging
        service = Service(
            log_path='/tmp/geckodriver.log'
        )

        try:
            driver = webdriver.Firefox(
                options=options,
                service=service
            )
            logger.info("Firefox driver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Firefox driver error: {str(e)}")
            try:
                version = subprocess.check_output([firefox_path, '--version'])
                logger.info(f"Firefox version: {version.decode().strip()}")
            except Exception as fe:
                logger.error(f"Error checking Firefox version: {str(fe)}")
            raise
    else:
        raise ValueError("Unsupported browser: {}".format(browser_name))

    return driver


def run_auth_flow(auth_url: str, brand: str = "CHEVROLET") -> str:
    """Run through the Smartcar authentication flow using Selenium.

    Args:
        auth_url: The authentication URL to start the flow
        brand: The vehicle brand to select (default: "CHEVROLET")

    Returns:
        str: The authorization code from the callback URL

    Raises:
        TimeoutException: If any element is not found within the timeout period
        WebDriverException: If there are any issues with the browser automation
    """
    logger = logging.getLogger(__name__)
    driver = None
    try:
        driver = get_driver(BROWSER, headless=HEADLESS)
        logger.info("Starting auth flow for brand: %s", brand)

        # Navigate to auth URL
        driver.get(auth_url)

        # Handle preamble
        logger.debug("Waiting for preamble button")
        preamble_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button#continue-button"))
        )
        preamble_button.click()

        # Select brand
        logger.debug("Selecting brand: %s", brand)
        brand_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"button#{brand.upper()}.brand-list-item")
            )
        )
        brand_button.click()

        # Handle login
        logger.debug("Handling login")
        username = f"{uuid.uuid4()}@email.com"
        sign_in_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "sign-in-button"))
        )
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys("password")
        sign_in_button.click()

        # Handle permissions
        logger.debug("Handling permissions approval")
        permissions_approval_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "approval-button"))
        )
        permissions_approval_button.click()

        # Wait for redirect
        WebDriverWait(driver, 30).until(EC.url_matches("example.com"))

        # Get authorization code
        url = driver.current_url
        code = get_code_from_url(url)
        logger.info("Successfully completed auth flow")
        return code

    except Exception as e:
        logger.error("Error during auth flow: %s", str(e))
        raise

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.warning("Error closing browser: %s", str(e))
