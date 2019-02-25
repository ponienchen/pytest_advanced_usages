"""

"""
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.python import Function


def pytest_addoption(parser):
    """
    For option arguments, see 'class Action(_AttributeHolder)'
    in ~/.pyenv/versions/3.7.0/lib/python3.7/argparse.py
    """
    parser.addoption(
        '--env',
        action='store',
        default='prod',
        help='environment value, defaulting to "prod"',
        choices=[
            'prod', 'qa'
        ]
    )


@pytest.fixture(scope='session')
def env(request: FixtureRequest):
    return request.config.getoption('--env')


def pytest_generate_tests(metafunc):
    params = metafunc.cls.local if hasattr(metafunc.cls, 'local') else []
    if not params:
        return
    metafunc.parametrize(
        argnames='output',
        argvalues=params,
        indirect=True
    )


def pytest_collection_modifyitems(session, config, items: [Function]):
    deselected = []
    selected = []
    for item in items:
        if not hasattr(item, 'callspec') or 'output' not in item.callspec.params:
            item.add_marker(pytest.mark.skip(reason='interface missing'))
            item.add_marker(pytest.mark.interface_missing)
            deselected.append(item)
        selected.append(item)
    config.hook.pytest_deselected(items=deselected)
    items[:] = selected


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    rep = outcome.get_result()
    extra = getattr(rep, 'extra', [])
    if rep.when == 'setup':
        if item.get_closest_marker('interface_missing'):
            rep.sections.append(
                (
                    'Warning',
                    f'There are missing interfaces. Please be sure to define local/remote in '
                    f'your test class(es)\n',
                )
            )
            rep.sections.append(
                (
                    'How to set up local/remote in your test class(es)?',
                    f'local = [LocalDesktopInterface.chrome]\n'
                    f'remote = [RemoteDesktopInterface.chrome]',
                )
            )
            extra.append(pytest_html.extras.url('http://www.example.com/'))
            extra.append(pytest_html.extras.text('This is Peter\'s Texts'))
            rep.extra = extra
