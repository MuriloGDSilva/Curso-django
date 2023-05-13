from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

ROOT_PATH = Path(__file__).parent.parent
CHROMEDIVER_NAME = 'chromedriver.exe'
CHROMEDIVER_PATH = ROOT_PATH / 'bin' / CHROMEDIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless', '--log-level=1')
    browser.get('http://www.google.com')
    sleep(10)
    browser.quit()
