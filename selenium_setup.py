from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time


class Browsers:
    CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"


class SeleniumScraper:

    def __init__(self, browser: str = Browsers.FIREFOX):
        self.browser = browser
        self.options = None
        self.service = None
        self.current_url = None
        self.previous_url = None

    def setup_chrome(self):
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.options = ChromeOptions()

    def setup_edge(self):
        self.service = EdgeService(
            executable_path=EdgeChromiumDriverManager().install()
        )
        self.options = EdgeOptions()

    def setup_firefox(self):
        self.service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.options = FirefoxOptions()

    def setup_browser(self):
        browser_methods = {
            "chrome": self.setup_chrome,
            "edge": self.setup_edge,
            "firefox": self.setup_firefox,
        }
        browser_methods[self.browser]()

    def open_browser(self, wait_seconds=0):
        self.setup_browser()
        browser_methods = {
            "chrome": self.open_chrome,
            "edge": self.open_edge,
            "firefox": self.open_firefox,
        }
        browser_methods[self.browser]()
        if wait_seconds > 0:
            time.sleep(wait_seconds)

    def open_chrome(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def open_edge(self):
        self.driver = webdriver.Edge(service=self.service, options=self.options)

    def open_firefox(self):
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

    def go_to_url(self, url):
        self.previous_url = self.current_url
        self.driver.get(url)
        self.current_url = url

    def close_browser(self):
        self.driver.close()

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, 1000000)")
