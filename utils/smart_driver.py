import os

from appium import webdriver

CWD = os.getcwd()
SCREEN_SHOTS_PATH = CWD + "/reports/screenshots/"

__driver_configs = {}


def driver_setup(host, port, platform_name, device_name, test_name, app_uri, automation_name):
    __driver_configs['host'] = host
    __driver_configs['port'] = port
    __driver_configs['platform_name'] = platform_name
    __driver_configs['device_name'] = device_name
    __driver_configs['test_name'] = test_name
    __driver_configs['app_uri'] = app_uri
    __driver_configs['automation_name'] = automation_name


def start_driver(context):
    try:
        context.driver = webdriver.Remote(
            command_executor='http://%s:%s/wd/hub' % (__driver_configs.get('host'), __driver_configs.get('port')),
            desired_capabilities={
                'platformName': __driver_configs.get('platform_name'),
                'platformVersion': __driver_configs.get('platform_version'),
                'deviceName': __driver_configs.get('device_name'),
                'app': (CWD + __driver_configs.get('app_uri'))
            })

        context.platform = __driver_configs.get('platform_name')
        if context.platform == 'Android':
            from pages.android.reddit_home_page import RedditHomePage
        elif context.platform == 'iOS':
            from pages.ios.reddit_home_page import RedditHomePage
        else:
            raise RuntimeError('Unrecognized platform: {}'.format(context.platform))
        context.reddit_home_page = RedditHomePage(context.driver)
    except Exception as e:
        raise e


def take_screenshot(context, filename):
    # ts = time.time()
    # st = time.ctime(ts)
    # screenshot_file =  SCREEN_SHOTS_PATH + filename + st + ".PNG"

    context.driver.save_screenshot(filename)


def cleanup_driver(context):
    context.driver.quit()


def teardown_driver(context):
    context.driver.quit()
