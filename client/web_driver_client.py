from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utils.constants import WebDriverClientConstant
from utils.helpers import SelectorParser, BrowserNameParser


class WebDriverClient:

    SUPPORTED_BROWSERS = WebDriverClientConstant.SUPPORTED_BROWSERS
    TIMEOUT = WebDriverClientConstant.TIME_OUT

    def __init__(self, browser: str = 'chrome'):
        browser = browser.lower()
        if browser not in self.SUPPORTED_BROWSERS:
            raise NotImplementedError(
                f'ERROR: You are trying to use "{browser}", '
                f'but currently only "{self.SUPPORTED_BROWSERS}" are supported.'
            )

        self.webdriver = getattr(webdriver, BrowserNameParser.parse_browser_name(browser))(
            service_args=(
                WebDriverClientConstant.SERVICE_ARGS.get(browser)
                if WebDriverClientConstant.ENABLE_LOGS
                else None
            )
        )

    def open_page(self, path: str):
        self.webdriver.get(path)

    def locator_parser(self, prefixed_locator: str) -> SelectorParser:
        if '=' not in prefixed_locator:
            raise AssertionError(
                f'ERROR: Expecting locator to be prefixed with locator type. Ex: css=...'
            )
        parts = prefixed_locator.split('=')
        return SelectorParser(*parts)

    def get_element(self, prefixed_locator: str) -> WebElement:
        locator_metadata = self.locator_parser(prefixed_locator)
        web_element = self.webdriver.find_element(*locator_metadata)
        return web_element

    def wait_until_visible(self, prefixed_locator: str) -> WebElement:
        locator_metadata = self.locator_parser(prefixed_locator)
        return WebDriverWait(self.webdriver, timeout=self.TIMEOUT).until(
            expected_conditions.visibility_of_element_located(locator_metadata)
        )

    def execute_js(self, script, *args):
        self.webdriver.execute_script(script, *args)

    def quit(self):
        if self.webdriver:
            self.webdriver.quit()
