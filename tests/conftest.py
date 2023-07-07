"""
Initializing Browser
Create base class which inherit setup class
Capture screenshot for failed test cases
Attach screenshot to the allure report
python add_option function which help the user to choose the browser at the run time
"""
import logging
import os

from config import (
    BASE_DIR,
    BrowserEnum,
    ClientEnum,
    EnvironmentEnum,
    LoggingLevelEnum,
)


import time
from datetime import datetime

import allure
import pytest

from allure_commons.types import AttachmentType
from dotenv import find_dotenv
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = None


def pytest_addoption(parser):
    # Accept browser name.
    parser.addoption(
        "--browser",
        action="store",
        default=BrowserEnum.CHROME.value[0],
        help=f"Choose from: {','.join([e.value[0] for e in BrowserEnum])}.",
    )

    # Accept which client to run for.
    parser.addoption(
        "--client",
        action="store",
        default=ClientEnum.LEVELUP.value[0],
        help=f"Choose from: {','.join([e.value[0] for e in ClientEnum])}",
    )

    # Accept which environment to run for.
    parser.addoption(
        "--env",
        action="store",
        default=EnvironmentEnum.PRODUCTION.value[0],
        help=f"Choose from: {','.join([e.value[0] for e in EnvironmentEnum])}",
    )

    # Accept logging level.
    parser.addoption(
        "--logging",
        action="store",
        default=LoggingLevelEnum.INFO.value[0],
        help=f"Choose from: {','.join([e.value[0] for e in LoggingLevelEnum])}",
    )

    # Accept if you want to execute in headless mode
    parser.addoption(
        "--headless", action="store", default="false", help=f"Choose from: true, false"
    )

def validate_cli_inputs(request):
    if not BrowserEnum.has_value(request.config.getoption("browser")):
        raise Exception(
            f"Browser name can only accept following values {', '.join([e.value[0] for e in BrowserEnum])}"
        )

    if not ClientEnum.has_value(request.config.getoption("client")):
        raise Exception(
            f"Client can only accept following values {','.join([e.value[0] for e in ClientEnum])}"
        )

    if not EnvironmentEnum.has_value(request.config.getoption("env")):
        raise Exception(
            f"Environment can only accept following values {','.join([e.value[0] for e in EnvironmentEnum])}"
        )

    if not LoggingLevelEnum.has_value(request.config.getoption("logging")):
        raise Exception(
            f"Logging level can only accept following values {','.join([e.value[0] for e in LoggingLevelEnum])}"
        )

def setupLogger(request, client_name, env_name):
    logging.getLogger(f"advisor-automation-{client_name}-{env_name}").setLevel(
        request.config.getoption("logging")
    )


def load_env_file(client_name, env_name):
    load_dotenv(find_dotenv(filename=f".env-{client_name}-{env_name}"))
    logging.debug("Expected .env=", f".env-{client_name}-{env_name}")


@pytest.fixture(scope="session", autouse=True)
def setup(request):
    current_env = request.config.getoption("env")
    pytest.current_client = request.config.getoption("client")
    browser_name = request.config.getoption("browser")
    verbose = request.config.getoption("logging") == LoggingLevelEnum.DEBUG.value[0]
    # set_grouping(parser, request)

    # Setting language globally
    # pytest.language = request.config.getoption("language")
    # Initialize the config
    validate_cli_inputs(request)
    load_env_file(pytest.current_client, current_env)
    setupLogger(request, pytest.current_client, current_env)

    browser_options = Options()
    browser_options.add_argument("--no-sandbox")
    browser_options.add_argument("--disable-dev-shm-usage")
    browser_options.add_experimental_option("useAutomationExtension", False)
    browser_options.add_argument("window-size=1920x1480")
    browser_options.add_argument("--use-fake-device-for-media-stream")
    browser_options.add_argument("--use-fake-ui-for-media-stream")
    # browser_options.add_argument("--use-file-for-fake-video-capture=/home/tanvijoshi/advisor-automation-pytest/video.y4m")
    browser_options.add_experimental_option("prefs",
                                            {"profile.default_content_setting_values.media_stream_mic": 1,
                                             "profile.default_content_setting_values.media_stream_camera": 1,
                                             "profile.default_content_setting_values.notifications": 1
                                             })

    if request.config.getoption("headless") == "true":
        browser_options.add_argument("--headless")

    # Setup the browsers
    if browser_name == BrowserEnum.CHROME.value[0]:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=browser_options,
        )
    elif browser_name == BrowserEnum.FIREFOX.value[0]:
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            verbose=verbose,
            options=browser_options,
        )
    elif browser_name == BrowserEnum.EDGE.value[0]:
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            verbose=verbose,
            options=browser_options,
        )

    # elif browser_name == BrowserEnum.SAFARI.value[0]:
    #     driver = webdriver.Safari(service=SafariService(GeckoDriverManager().install(), options=browser_options))

    else:
        raise Exception("This browser is not supported.")

    #for session level driver initiation
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)

    driver.maximize_window()
    driver.implicitly_wait(5), """Wait for 5 sec to load whole page"""
    # request.cls.driver = driver # can be used when scope=class
    yield driver
    driver.quit()


# Set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


# Check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node is an "item" because we use the default "function" scope
    if request.node.rep_setup.failed:
        print("Setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs["setup"]
            take_screenshot(driver, request.node.nodeid)
            print("Executing a test failed.", request.node.nodeid)


def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}{datetime.today().strftime("%Y-%m-%d%H:%M")}'.replace(
        "/", "_"
    ).replace("::", "_")
    file_name = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    driver.save_screenshot(os.path.join(BASE_DIR, "screenshots", file_name) + ".png")
    allure.attach(
        driver.get_screenshot_as_png(),
        name="Screenshot",
        attachment_type=AttachmentType.PNG,
    )