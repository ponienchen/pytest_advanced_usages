from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement

from client.web_driver_client import WebDriverClient


class PageBase(ABC):

    def __init__(self, webdriver_client: WebDriverClient):
        self.webdriver_client = webdriver_client

    @abstractmethod
    def _required_elements(self) -> list:
        raise NotImplementedError(
            f'ERROR: Method not implemented!'
        )

    def wait_until_all_required_elements_visible(self) -> bool:
        return all(
            [self.webdriver_client.wait_until_visible(e) for e in self._required_elements()]
        )

    def clear_and_type(self, web_element: WebElement, text: str):
        self.webdriver_client.execute_js('arguments[0].focus()', web_element)
        self.webdriver_client.execute_js('arguments[0].value = ""', web_element)
        web_element.send_keys(text)
