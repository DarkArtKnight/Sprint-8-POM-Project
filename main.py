import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import helpers  # Assumes helpers.py is in the same directory
from pages import UrbanRoutesPage  # Assuming pages.py is in a 'pages' package


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        """Sets up the browser driver with logging capabilities as instructed."""
        # This 'if' statement is moved here as per the project instructions.
        if not helpers.is_url_reachable(helpers.URBAN_ROUTES_URL):
            pytest.skip("Urban Routes URL is not reachable. Skipping tests.")

        # This setup is explicitly required by the task description.
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        # An implicit wait can be useful here if not using explicit waits everywhere.
        cls.driver.implicitly_wait(5)

    def test_full_order_flow(self):
        """Runs the full end-to-end test for ordering a taxi."""
        self.driver.get(helpers.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)

        # Step 1: Set address and call a taxi
        page.set_address_from("East 2nd Street, 601")
        page.set_address_to("1300 1st St")
        page.click_call_taxi_button()

        # Step 2: Select Supportive tariff
        page.select_supportive_tariff()

        # Step 3: Set phone number and get/enter SMS code
        phone_number = helpers.generate_random_phone_number()
        page.enter_phone_number_and_proceed(phone_number)

        sms_code = helpers.retrieve_phone_code(self.driver)
        page.enter_phone_code_and_confirm(sms_code)

        # Step 4: Add a credit card
        card_number, card_code = helpers.generate_random_card_data()
        page.add_credit_card(card_number, card_code)

        # Step 5: Write a comment for the driver
        page.set_comment("Please be on time. Thank you!")

        # Step 6: Order Blanket and Handkerchiefs and verify
        page.select_blanket_and_handkerchiefs()
        assert page.is_blanket_selected(), "Blanket and handkerchiefs switch was not selected."

        # Step 7: Order 2 Ice Creams and verify
        page.add_ice_creams(2)
        assert page.get_ice_cream_count() == 2, "Ice cream count is not 2."

        # Step 8: Order the taxi
        page.click_order_button()

        # Step 9: Verify the car search modal appears
        assert page.is_car_search_modal_displayed(), "Car search modal did not appear after ordering."

    @classmethod
    def teardown_class(cls):
        """Closes the browser after all tests have finished."""
        # The 'if' check is a safe programming practice but can be removed if you prefer.
        if cls.driver:
            cls.driver.quit()
