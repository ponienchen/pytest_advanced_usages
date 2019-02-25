from client.web_driver_client import WebDriverClient
from pages.page_base import PageBase
from utils.config_loader import ConfigLoader


class Homepage(PageBase):

    INPUT_WHAT = 'css=#text-input-what'
    INPUT_WHERE = 'css=#text-input-where'
    FIND_JOBS = 'css=.icl-WhatWhere-buttonWrapper button'

    def __init__(self, env: str, webdriver_client: WebDriverClient):
        super().__init__(webdriver_client)
        self.config_loader = ConfigLoader()
        self.base_url = self.config_loader.get_value(env, 'root')

    def type_in_what(self, text: str):
        web_element = self.webdriver_client.wait_until_visible(self.INPUT_WHAT)
        self.clear_and_type(web_element, text)

    def type_in_where(self, text: str):
        web_element = self.webdriver_client.wait_until_visible(self.INPUT_WHERE)
        self.clear_and_type(web_element, text)

    def click_find_jobs_button(self):
        web_element = self.webdriver_client.wait_until_visible(self.FIND_JOBS)
        web_element.click()

    def open(self):
        self.webdriver_client.open_page(self.base_url)
        self.wait_until_all_required_elements_visible()

    def _required_elements(self) -> list:
        return [
            self.INPUT_WHAT,
            self.INPUT_WHERE,
            self.FIND_JOBS
        ]
