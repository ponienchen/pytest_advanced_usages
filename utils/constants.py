class WebDriverClientConstant:

    ENABLE_LOGS = True
    LOGS_FOLDER = '../logs'
    CHROME_DRIVER_LOG = f'{LOGS_FOLDER}/chromedriver.log'
    SUPPORTED_BROWSERS = ['chrome']
    TIME_OUT = 5  # in seconds
    SERVICE_ARGS = {
        'chrome': [
            '--verbose',
            f'--log-path={CHROME_DRIVER_LOG}'
        ]
    }


class JobType:

    JOBS = [
        'qa',
        'developer',
        'driver',
        'pilot'
    ]


class CityType:

    CITIES = [
        'San Francisco, CA',
        'Oakland, CA',
        'Fremont, CA'
    ]
