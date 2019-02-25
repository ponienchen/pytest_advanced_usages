import pytest
from _pytest.fixtures import FixtureRequest

from client.web_driver_client import WebDriverClient
from pages.homepage import Homepage


class TestOne:

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
        'address',
        ['12345 Heaven Ave, Oakland, CA 99876']
    )
    def test_do_a_lot(
            self,
            output: str,
            address: str
    ):
        print('\ntest that does a lot')
        print(f'output: {output}, address: {address}\n')

    @pytest.mark.usefixtures('output')
    def test_do_little(self):
        print('\ntest that does little\n')
