import random

import pytest
from _pytest.fixtures import FixtureRequest

from client.web_driver_client import WebDriverClient
from pages.homepage import Homepage
from utils.constants import JobType, CityType


class TestHomepage:

    # local = [
    #     'Dummy-Link'
    # ]

    @pytest.fixture(name='output')
    def selenium_fixture(self, request: FixtureRequest) -> str:
        output = f'\n-- {request.param} --'
        return output

    @pytest.fixture(autouse=True)
    def pre_test_setup(self, env: str, request: FixtureRequest):
        self.webdriver_client = WebDriverClient()
        self.homepage = Homepage(env, self.webdriver_client)
        request.addfinalizer(
            self.teardown
        )

    def teardown(self):
        if hasattr(self, 'webdriver_client'):
            self.webdriver_client.quit()

    @pytest.mark.parametrize(
        'another',
        [1]
    )
    def test_perform_one_super_basic_search_without_checking_search_results(
            self,
            output: str,
            another: int
    ):
        print(f'output: {output}')
        # self.homepage.open()
        # job = random.choice(JobType.JOBS)
        # city = random.choice(CityType.CITIES)
        # self.homepage.type_in_what(job)
        # self.homepage.type_in_where(city)
        # self.homepage.click_find_jobs_button()
