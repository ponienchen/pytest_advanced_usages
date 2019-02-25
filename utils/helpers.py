from typing import NamedTuple


class SelectorParser(NamedTuple):
    selector_type: str
    locator: str


class BrowserNameParser:

    @staticmethod
    def parse_browser_name(name: str) -> str:
        return name.capitalize()
