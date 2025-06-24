import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import BASE_URL
from utils.logger import get_logger

logger = get_logger()

class HomePage:
    URL = f"{BASE_URL}/"

    def __init__(self, driver):
        self.driver = driver

    def go(self):
        logger.info("Navigating to home page")
        self.driver.get(self.URL)

    def verify_home_page(self):
        try:
            logger.info(f"Checking HTTP status code for {self.URL}")
            response = requests.get(self.URL, timeout=10)
            if response.status_code != 200:
                logger.error(f"❌ Status code is {response.status_code}, expected 200")
                return False
            logger.info("✅ Status code is 200")

            current_url = self.driver.current_url
            logger.info(f"Checking current URL: {current_url}")
            if not current_url.startswith(self.URL):
                logger.error(f"❌ Current URL mismatch.\nExpected: starts with '{self.URL}'\nFound:    '{current_url}'")
                return False
            logger.info("✅ Current URL is correct")

            logger.info("Looking for meta tag: og:site_name")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//meta[@property='og:site_name']"))
                )
            except Exception:
                logger.error("❌ Meta tag with property='og:site_name' not found in DOM.")
                return False

            try:
                content = self.driver.find_element(By.XPATH, "//meta[@property='og:site_name']").get_attribute("content")
            except Exception:
                logger.error("❌ Meta tag element was located but content attribute could not be read.")
                return False

            logger.info(f"Meta content found: '{content}'")
            if content != "Insider":
                logger.error(f"❌ Meta content mismatch.\nExpected: 'Insider'\nFound:    '{content}'")
                return False
            logger.info("✅ Meta tag content is 'Insider'")

            return True

        except Exception as e:
            logger.error(f"❌ Unexpected exception during home page verification: {e}")
            return False
