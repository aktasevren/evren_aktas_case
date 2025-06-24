from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
import time
from selenium.common.exceptions import NoSuchElementException

logger = get_logger()

class CareersPage:
    COMPANY_MENU = (By.XPATH, "//a[@id='navbarDropdownMenuLink' and contains(text(), 'Company')]")
    CAREERS_LINK = (By.XPATH, "//a[@href='https://useinsider.com/careers/' and text()='Careers']")
    TEAM_CARD = (By.CSS_SELECTOR, "div.job-item")
    SEE_ALL_TEAMS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all teams')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_careers_page(self):
        try:
            logger.info("Hovering over 'Company' menu")
            company_element = self.wait.until(EC.presence_of_element_located(self.COMPANY_MENU))
            ActionChains(self.driver).move_to_element(company_element).perform()

            logger.info("Waiting for 'Careers' link to appear")
            careers_link = self.wait.until(EC.element_to_be_clickable(self.CAREERS_LINK))

            logger.info("Clicking 'Careers' link")
            careers_link.click()
            time.sleep(2)
            self.driver.execute_script("document.body.style.zoom='80%'")


            logger.info("✅ Navigated to Careers page")
        except Exception as e:
            logger.error(f"❌ Failed to navigate to Careers page: {e}")
            raise

    def count_team_cards(self):
        try:
            initial_teams = self.driver.find_elements(*self.TEAM_CARD)
            visible_count = len(initial_teams)
            logger.info(f"🟢 Initially visible team count: {visible_count}")

            try:
                see_all_btn = self.wait.until(EC.element_to_be_clickable(self.SEE_ALL_TEAMS_BUTTON))
                logger.info("Clicking 'See all teams' button to load full list")
                
                for y in range(0, 2000, 200):
                    self.driver.execute_script(f"window.scrollTo(0, {y});")
                    time.sleep(0.5)

                    try:
                        see_all_btn = self.driver.find_element(*self.SEE_ALL_TEAMS_BUTTON)
                        if see_all_btn.is_displayed():
                            logger.info(f"🎯 'See all teams' button became visible at scroll position: {y}")
                            self.driver.execute_script("arguments[0].click();", see_all_btn)
                            logger.info("✅ Successfully clicked 'See all teams' button.")
                            break
                    except Exception as e:
                        logger.debug(f"🔍 Scrolling to {y}px — button not visible yet.")
                else:
                    logger.warning("⚠️ 'See all teams' button was not found after scrolling.")
                
                time.sleep(1)

                self.wait.until(lambda d: len(d.find_elements(*self.TEAM_CARD)) > visible_count)
                all_teams = self.driver.find_elements(*self.TEAM_CARD)
                total_count = len(all_teams)

                logger.warning(f"⚠️ Total team count after expansion: {total_count}")
                logger.warning(f"⚠️ {total_count - visible_count} new teams loaded after clicking 'See all teams'")

            except Exception as err:
                logger.info("No 'See all teams' button found or already fully loaded.")
                logger.info(err)
                total_count = visible_count
            return visible_count, total_count
        except Exception as e:
            logger.error(f"❌ Failed to count team sections: {e}")
            return 0, 0
        


    def verify_locations_block(self):
        try:
            logger.info("🔍 Checking 'Our Locations' section")
            location_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Our Locations')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", location_header)
            time.sleep(1)
            logger.info("✅ 'Our Locations' section is present and in view")

            initial_city_elements = self.driver.find_elements(By.CSS_SELECTOR, ".location-info > p")
            initial_cities = [el.text.strip() for el in initial_city_elements if el.text.strip()]
            initial_count = len(set(initial_cities))
            logger.info(f"🟢 Initially visible city count: {initial_count}")
            next_arrow = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-arrow-right.location-slider-next"))
            )

            all_cities = set(initial_cities)
            max_scrolls = 30
            scroll_count = 0

            while scroll_count < max_scrolls:
                try:
                    self.driver.execute_script("arguments[0].click();", next_arrow)
                    time.sleep(0.4)
                    city_elements = self.driver.find_elements(By.CSS_SELECTOR, ".location-info > p")
                    for el in city_elements:
                        city = el.text.strip()
                        if city:
                            all_cities.add(city)

                    if len(all_cities) >= 28:
                        break

                except Exception as e:
                    logger.warning(f"⚠️ Scroll attempt {scroll_count + 1} failed: {e}")
                    break

                scroll_count += 1

            logger.info(f"📊 Unique cities collected after scroll: {len(all_cities)}")
            for idx, city in enumerate(sorted(all_cities), 1):
                logger.info(f"📍 Location {idx}: {city}")

            return initial_count, len(all_cities)

        except Exception as e:
            logger.error(f"❌ Exception in verifying locations block: {e}")
            return 0, 0

    def verify_life_at_insider_block(self):
        try:
            logger.info("🔍 Checking 'Life at Insider' section")
            life_header = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Life at Insider')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", life_header)
            time.sleep(1)
            logger.info("✅ 'Life at Insider' section is present and in view")
            all_slides = self.driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide[data-swiper-slide-index]")
            unique_indices = set()

            for slide in all_slides:
                idx = slide.get_attribute("data-swiper-slide-index")
                if idx is not None:
                    unique_indices.add(idx)

            total = len(unique_indices)
            visible_slides = [
                slide for slide in all_slides
                if any(cls in slide.get_attribute("class") for cls in ["swiper-slide-prev", "swiper-slide-active", "swiper-slide-next"])
            ]
            visible = len(visible_slides)

            logger.info(f"🖼️ Total unique slides (based on index): {total}")
            logger.info(f"👁️ Initially visible slides: {visible}")

            return visible, total

        except Exception as e:
            logger.error(f"❌ Failed to verify 'Life at Insider' section: {e}")
            return 0, 0






    # TEAMS_BLOCK = (By.CSS_SELECTOR, "div.elementor-element-b6c45b2")
    # LIFE_BLOCK = (By.CSS_SELECTOR, "section.elementor-element-a8e7b90")
    # LOCATIONS_BLOCK = (By.CSS_SELECTOR, "section.elementor-element-8ab30be")

    # def are_elementor_blocks_displayed(self):
    #     blocks = {
    #         "Block 1 (div.b6c45b2)": self.TEAMS_BLOCK,
    #         "Block 2 (section.a8e7b90)": self.LIFE_BLOCK,
    #         "Block 3 (section.8ab30be)": self.LOCATIONS_BLOCK,
    #     }

    #     results = {}

    #     for name, locator in blocks.items():
    #         try:
    #             element = self.wait.until(EC.presence_of_element_located(locator))
    #             is_displayed = element.is_displayed()
    #             logger.info(f"✅ {name} is_displayed = {is_displayed}")
    #             results[name] = is_displayed
    #         except NoSuchElementException:
    #             logger.error(f"❌ {name} not found on the page.")
    #             results[name] = False
    #         except Exception as e:
    #             logger.error(f"❌ Error checking {name}: {e}")
    #             results[name] = False

    #     return results
