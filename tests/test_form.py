import requests
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.form_page import FormPage

UAE_PROXY = "3.28.119.118:8888"

UAE_REQUESTS_PROXIES = {
    'http': '3.28.119.118:8888',
    'https': '3.28.119.118:8888',
}

DUBAI_POLICE_PAGE_URL = "https://hh.dtcm.gov.ae/holidayhomes/Welcome.aspx"
IF_CONFIG_ME_URL = "https://ifconfig.me"


@pytest.fixture()
def driver_with_proxy():
    driver_service = Service(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % UAE_PROXY)
    web_driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    web_driver.maximize_window()
    yield web_driver
    web_driver.quit()


class TestChromeWebDriver:
    def test_form_if_config_me(self, driver_with_proxy):
        form_page = FormPage(driver=driver_with_proxy, url=IF_CONFIG_ME_URL)
        form_page.open()

    def test_dubai_police_page(self, driver_with_proxy):
        form_page = FormPage(driver=driver_with_proxy, url=DUBAI_POLICE_PAGE_URL)
        form_page.open()
        assert 1


class TestHTTPRequests:
    """
    CURL:
        curl -x 3.28.119.118:8888 https://hh.dtcm.gov.ae/holidayhomes/Welcome.aspx
    """
    def test_if_config_me(self):
        response = requests.get(IF_CONFIG_ME_URL, proxies=UAE_REQUESTS_PROXIES)
        assert response.status_code == 200
        assert response.text == '3.28.119.118'  # dubai location

    def test_dubai_police_page(self):
        response = requests.get(DUBAI_POLICE_PAGE_URL, proxies=UAE_REQUESTS_PROXIES)
        assert response.status_code == 200
