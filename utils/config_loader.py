from configparser import ConfigParser


class ConfigLoader:

    def __init__(self, file_path: str = '../conf/url.ini'):
        self.parser = ConfigParser()
        self.parser.read(file_path)
        self.file_path = file_path

    def get_value(self, section: str, option: str) -> str:
        if section not in self.parser.sections():
            raise AssertionError(
                f'"{section}" is not a valid section in "{self.file_path}"'
            )

        if option not in self.parser.options(section):
            raise AssertionError(
                f'"{option}" is not defined under the section "{section}"'
            )

        target_value = next(
            (value for name, value in self.parser.items(section) if name == option)
        )
        return target_value
