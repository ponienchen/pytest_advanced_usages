"""

"""
import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.python import Function
from _pytest.reports import TestReport


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


def pytest_collection_modifyitems(config, items: [Function]):
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
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    rep = outcome.get_result()
    extra = getattr(rep, 'extra', [])
    if rep.when == 'setup':
        if item.get_closest_marker('interface_missing'):
            rep.sections.append(
                (
                    '========== Warning ==========',
                    f'There are missing interfaces. Please be sure to define local/remote in '
                    f'your test class(es)\n\n'
                    f'Example:\n'
                    f'  local = [\n'
                    f'      LocalDesktopInterface.chrome\n'
                    f'  ]\n'
                    f'  remote = [\n'
                    f'      RemoteDesktopInterface.chrome\n'
                    f'  ]\n'
                )
            )
            extra.append(pytest_html.extras.url('http://www.example.com/'))
            extra.append(pytest_html.extras.text('This is Peter\'s Texts'))
            rep.extra = extra


def pytest_terminal_summary(terminalreporter):
    target_reports = []
    for report_list in terminalreporter.stats.values():
        for rep in report_list:
            if (
                    'interface_missing' in list(rep.keywords)
                    and isinstance(rep, TestReport)
                    and rep.when == 'setup'
            ):
                target_reports.extend([rep])
    if not target_reports:
        return

    terminalreporter.write_line('')
    terminalreporter.write_sep('=', 'Interface Missing Warning')
    terminalreporter.write_line(f'Total affected tests count: {len(target_reports)}\n')
    for rep in target_reports:
        terminalreporter.write_line(f'{rep.nodeid}')
        for sec in rep.sections:
            for text in sec:
                terminalreporter.write_line(text)
        terminalreporter.write_line('')
