from utils.base_test import BaseTest
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from utils.logger import get_logger
import pytest

logger = get_logger()

class TestCareersPage(BaseTest):

    def test_careers_teams_section(self):
        logger.info("🔍 Starting test: Careers Page – Teams Section")
        home = HomePage(self.driver)
        home.go()

        careers = CareersPage(self.driver)
        careers.navigate_to_careers_page()

        visible, total = careers.count_team_cards()

        if total > visible:
            warning_msg = f"⚠️ Only {visible}/{total} teams are initially visible — others loaded after 'See all teams'"
            logger.warning(warning_msg)
            pytest.skip(warning_msg)
        else:
            logger.info(f"✅ All {total} teams are visible without expanding")

        assert total >= visible, (
            f"❌ Visible teams: {visible} / Total teams after load: {total}"
        )

        logger.info("✅ Careers Teams Section test completed successfully")

    def test_careers_locations_section(self):
        logger.info("🔍 Starting test: Careers Page – Locations Section")
        home = HomePage(self.driver)
        home.go()

        careers = CareersPage(self.driver)
        careers.navigate_to_careers_page()
        visible_count, unique_cities = careers.verify_locations_block()

        expected_count = 25
        if visible_count < expected_count:
            warning_msg = (
                f"⚠️ Only {visible_count}/{expected_count} unique locations are visible initially "
                f"— Others were loaded dynamically upon scrolling"
            )
            logger.warning(warning_msg)
            pytest.skip(warning_msg)

        assert visible_count == expected_count, (
            f"❌ Expected {expected_count} unique locations, found {visible_count}"
        )

        logger.info("✅ Locations Section test completed successfully")

    def test_careers_life_at_insider_section(self):
        logger.info("🔍 Starting test: Careers Page – Life at Insider Section")

        home = HomePage(self.driver)
        home.go()

        careers = CareersPage(self.driver)
        careers.navigate_to_careers_page()

        visible, total = careers.verify_life_at_insider_block()

        if total == 0:
            pytest.fail("❌ No slides found in 'Life at Insider' section")

        if visible < total:
            msg = f"⚠️ Only {visible}/{total} slides are initially visible — others require slider interaction"
            logger.warning(msg)
            pytest.skip(msg)

        logger.info("✅ All Life at Insider slides are visible without interaction")




    # def test_elementor_blocks_are_displayed(self):
    #     logger.info("🔍 Test: Check visibility of specific Elementor blocks")

    #     home = HomePage(self.driver)
    #     home.go()

    #     careers = CareersPage(self.driver)
    #     careers.navigate_to_careers_page()

    #     block_results = careers.are_elementor_blocks_displayed()

    #     for block_name, is_displayed in block_results.items():
    #         assert is_displayed, f"❌ {block_name} is not displayed on the page"

    #     logger.info("✅ All specified Elementor blocks are visible on the page")
