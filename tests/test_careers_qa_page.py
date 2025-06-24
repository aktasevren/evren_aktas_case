from utils.base_test import BaseTest
from pages.careers_qa_page import CareersQAPage
from utils.logger import get_logger

logger = get_logger()

class TestCareersQA(BaseTest):

    def test_select_location(self):
        logger.info("Test: Location filter – Istanbul, Turkiye")
        qa_page = CareersQAPage(self.driver)
        qa_page.go_to_qa_page()
        qa_page.click_see_all_qa_jobs()

        location_select = qa_page.select_location("Istanbul, Turkiye")
        selected_location = location_select.first_selected_option.text.strip()

        assert selected_location == "Istanbul, Turkiye", f"Location selection failed! Got: {selected_location}"
        logger.info("Location selection passed")

    def test_select_department(self):
        logger.info("Test: Department filter – Quality Assurance")

        qa_page = CareersQAPage(self.driver)
        qa_page.go_to_qa_page()
        qa_page.click_see_all_qa_jobs()
        qa_page.select_location("Istanbul, Turkiye")

        department_select = qa_page.select_department("Quality Assurance")
        selected_department = department_select.first_selected_option.text.strip()

        assert selected_department == "Quality Assurance", f"Department selection failed! Got: {selected_department}"
        logger.info("Department selection passed")


    def test_verify_filtered_job_list(self):
        logger.info("Test: Verify filtered QA job list content")

        qa_page = CareersQAPage(self.driver)
        qa_page.go_to_qa_page()
        qa_page.click_see_all_qa_jobs()
        qa_page.select_location("Istanbul, Turkiye")
        qa_page.select_department("Quality Assurance")

        jobs = qa_page.get_all_job_cards()

        assert jobs, "No jobs found after applying filters"

        for idx, job in enumerate(jobs, 1):
            logger.info(f"Job {idx}: {job['title']} | {job['location']} | {job['department']}")
            assert job['location'] == "Istanbul, Turkiye", f"Job {idx} has invalid location: {job['location']}"
            assert job['department'] == "Quality Assurance", f"Job {idx} has invalid department: {job['department']}"

        logger.info("All filtered jobs have correct location and department")

    def test_view_role_redirect(self):
        logger.info("Test: View Role redirection")

        qa_page = CareersQAPage(self.driver)
        qa_page.go_to_qa_page()
        qa_page.click_see_all_qa_jobs()
        qa_page.select_location("Istanbul, Turkiye")
        qa_page.select_department("Quality Assurance")
        qa_page.click_specific_view_role()

        logger.info("🧭 Switching to newly opened tab")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        current_url = self.driver.current_url

        logger.info(f"New tab URL: {current_url}")
        assert "jobs.lever.co" in current_url, "Redirected URL is not a Lever application form"
        logger.info("View Role redirection passed")
