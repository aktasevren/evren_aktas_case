import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.base_test import BaseTest
from pages.home_page import HomePage
from utils.logger import get_logger

logger = get_logger()

class TestHomePage(BaseTest):
    def test_home_page_verification(self):
        logger.info("Starting test: Insider Home Page Verification")

        home = HomePage(self.driver)
        home.go()
        assert home.verify_home_page(), "Home page failed verification"

        logger.info("Home page test completed successfully")
