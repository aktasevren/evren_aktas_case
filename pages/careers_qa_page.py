from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger
import time
from selenium.webdriver.support.ui import Select

logger = get_logger()

class CareersQAPage:
    QA_PAGE_URL = "https://useinsider.com/careers/quality-assurance/"
    SEE_ALL_JOBS_BTN = (By.XPATH, "//a[contains(text(),'See all QA jobs')]")
    LOCATION_FILTER_DROPDOWN = (By.CSS_SELECTOR, "#select2-filter-by-location-container")
    DEPARMENT_FILTER_DROPDOWN = (By.CSS_SELECTOR, "#select2-filter-by-department-container")
    LOCATION_OPTION_TEMPLATE = "//li[contains(@id, 'select2-filter-by-location-result') and text()='{}']"
    BROWSE_OPEN_POSITIONS_HEADER = (By.XPATH, "//h3[contains(text(), 'Browse') and contains(text(), 'Open Positions')]") 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_qa_page(self):
        logger.info(f"🔗 Navigating to QA Careers page: {self.QA_PAGE_URL}")
        self.driver.get(self.QA_PAGE_URL)
        time.sleep(5)

    def click_see_all_qa_jobs(self):
        logger.info("🖱️ Clicking 'See all QA jobs' button")
        button = self.wait.until(EC.element_to_be_clickable(self.SEE_ALL_JOBS_BTN))
        button.click()
        time.sleep(3)

        for _ in range(1):
            self.driver.execute_script("document.body.style.zoom='80%'")
            self.driver.execute_script("window.scrollBy(0, 300);")
            time.sleep(6)

    def select_location(self, location_name="Istanbul, Turkiye"):
        try:
            logger.info(f"📍 Selecting location: {location_name}")
            select_element = self.wait.until(
                EC.presence_of_element_located((By.ID, "filter-by-location"))
            )
            time.sleep(5) 
            
            select = Select(select_element)
            select.select_by_visible_text(location_name)

            logger.info(f"✅ Location '{location_name}' selected")
            time.sleep(5) 
            return select
        except Exception as e:
            logger.error(f"❌ Failed to select location '{location_name}': {e}")
            raise

    def select_department(self, department_name="Quality Assurance"):
        try:
            logger.info(f"🖱️ Selecting department: {department_name}")
            
            select_element = self.wait.until(
                EC.presence_of_element_located((By.ID, "filter-by-department"))
            )
            time.sleep(5) 
            
            select = Select(select_element)
            select.select_by_visible_text(department_name)
            
            logger.info(f"✅ Department '{department_name}' selected")
            time.sleep(5) 
            return select

        except Exception as e:
            logger.error(f"❌ Failed to select department '{department_name}': {e}")
            raise

    def get_all_job_cards(self):
        logger.info("🔍 Retrieving filtered job cards")

        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".position-list-item-wrapper")))
        job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".position-list-item-wrapper")

        job_data = []
        for el in job_elements:
            try:
                title = el.find_element(By.CLASS_NAME, "position-title").text.strip()
                location = el.find_element(By.CLASS_NAME, "position-location").text.strip()
                department = el.find_element(By.CLASS_NAME, "position-department").text.strip()
                job_data.append({
                    "title": title,
                    "location": location,
                    "department": department
                })
            except Exception as e:
                logger.warning(f"⚠️ Failed to parse a job card: {e}")

        logger.info(f"🧾 Total job cards found: {len(job_data)}")
        return job_data

    def click_specific_view_role(self):
        try:
            logger.info("🔍 Looking for a job card with 'View Role' link")
            job_card = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".position-list-item-wrapper"))
            )
            view_role_btn = job_card.find_element(By.XPATH, ".//a[contains(text(), 'View Role')]")
            href = view_role_btn.get_attribute("href")

            logger.info(f"🌐 Navigating to job detail page: {href}")
            self.driver.execute_script(f"window.open('{href}', '_blank');")
            time.sleep(2)

            logger.info("✅ View Role URL opened in new tab")

        except Exception as e:
            logger.error(f"❌ Failed to open 'View Role' href: {e}")
            raise
