from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:

    # Locators
    FROM_LOCATOR = (By.ID, 'from')
    TO_LOCATOR = (By.ID, 'to')
    CALL_TAXI_BUTTON_LOCATOR = (By.XPATH, '//button[text()="Call a taxi"]')

    SUPPORTIVE_TARIFF_LOCATOR = (By.XPATH, '//div[contains(text(),"Supportive")]')
    SUPPORTIVE_TARIFF_ACTIVE_LOCATOR = (By.XPATH, '//div[contains(text(),"Supportive")]/ancestor::div[contains(@class, "card-selected")]')

    PHONE_NUMBER_FIELD_LOCATOR = (By.ID, 'phone')
    PHONE_NEXT_BUTTON_LOCATOR = (By.XPATH, '//div[@class="np-buttons"]//button[text()="Next"]')
    PHONE_CODE_FIELD_LOCATOR = (By.ID, 'code')
    PHONE_CONFIRM_BUTTON_LOCATOR = (By.XPATH, '//div[@class="pp-buttons"]//button[text()="Confirm"]')

    PAYMENT_METHOD_LINK_LOCATOR = (By.CLASS_NAME, 'pp-value-text')
    ADD_CARD_LINK_LOCATOR = (By.CLASS_NAME, 'pp-plus')
    CARD_NUMBER_FIELD_LOCATOR = (By.ID, 'number')
    CARD_CODE_FIELD_LOCATOR = (By.CSS_SELECTOR, 'input#code.card-input')  # Using a specific CSS selector from the task tip
    CARD_ADD_BUTTON_LOCATOR = (By.XPATH, '//div[@class="pp-form"]//button[text()="Link"]')
    PAYMENT_MODAL_CLOSE_BUTTON_LOCATOR = (By.XPATH,
                                          '//div[@class="payment-picker open"]//button[@class="close-button"]')

    COMMENT_FIELD_LOCATOR = (By.ID, 'comment')
    BLANKET_SWITCH_LOCATOR = (By.XPATH, '//label[text()="Blanket and handkerchiefs"]/preceding-sibling::div//input')
    ICE_CREAM_PLUS_BUTTON_LOCATOR = (By.XPATH, '//div[text()="Ice cream"]/parent::div//div[@class="counter-plus"]')
    ICE_CREAM_COUNTER_VALUE_LOCATOR = (By.XPATH, '//div[text()="Ice cream"]/parent::div//div[@class="counter-value"]')

    ORDER_BUTTON_LOCATOR = (By.XPATH, '//span[text()="Order"]/parent::button')
    CAR_SEARCH_MODAL_LOCATOR = (By.XPATH, '//div[text()="Car search"]')

    def __init__(self, driver):
        self.driver = driver

    # Methods
    def set_address_from(self, address):
        self.driver.find_element(*self.FROM_LOCATOR).send_keys(address)

    def set_address_to(self, address):
        self.driver.find_element(*self.TO_LOCATOR).send_keys(address)

    def click_call_taxi_button(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON_LOCATOR).click()

    def select_supportive_tariff(self):
        # find_elements returns a list. If the list is empty, the element wasn't found!
        if len(self.driver.find_elements(*self.SUPPORTIVE_TARIFF_ACTIVE_LOCATOR)) == 0:
            self.driver.find_element(*self.SUPPORTIVE_TARIFF_LOCATOR).click()

    def enter_phone_number_and_proceed(self, phone):
        # Enters the phone number and clicks "Next"
        self.driver.find_element(*self.PHONE_NUMBER_FIELD_LOCATOR).send_keys(phone)
        self.driver.find_element(*self.PHONE_NEXT_BUTTON_LOCATOR).click()

    def enter_phone_code_and_confirm(self, code):
        # Enters the SMS code and clicks "Confirm"
        self.driver.find_element(*self.PHONE_CODE_FIELD_LOCATOR).send_keys(code)
        self.driver.find_element(*self.PHONE_CONFIRM_BUTTON_LOCATOR).click()

    def add_credit_card(self, card_number, card_code):
        # A multistep method to add a credit card
        self.driver.find_element(*self.PAYMENT_METHOD_LINK_LOCATOR).click()
        self.driver.find_element(*self.ADD_CARD_LINK_LOCATOR).click()

        # Fill card details
        self.driver.find_element(*self.CARD_NUMBER_FIELD_LOCATOR).send_keys(card_number)
        card_code_field = self.driver.find_element(*self.CARD_CODE_FIELD_LOCATOR)
        card_code_field.send_keys(card_code)

        # Bug workaround explicitly mentioned in the task description
        card_code_field.send_keys(Keys.TAB)

        self.driver.find_element(*self.CARD_ADD_BUTTON_LOCATOR).click()
        self.driver.find_element(*self.PAYMENT_MODAL_CLOSE_BUTTON_LOCATOR).click()

    def set_comment(self, comment_text):
        self.driver.find_element(*self.COMMENT_FIELD_LOCATOR).send_keys(comment_text)

    def select_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_SWITCH_LOCATOR).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_SWITCH_LOCATOR).is_selected()

    def add_ice_creams(self, count):
        # Clicks the plus button for ice cream a specified number of times.
        # This moves the loop from the test script into the POM
        plus_button = self.driver.find_element(*self.ICE_CREAM_PLUS_BUTTON_LOCATOR)
        for _ in range(count):
            plus_button.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNTER_VALUE_LOCATOR).text)

    def click_order_button(self):
        self.driver.find_element(*self.ORDER_BUTTON_LOCATOR).click()

    def is_car_search_modal_displayed(self):
        # Returns True if the car search modal is displayed
        return len(self.driver.find_elements(*self.CAR_SEARCH_MODAL_LOCATOR)) > 0
