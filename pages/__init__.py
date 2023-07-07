"""
__________________________________________________
Base Page that provides basic page functionality
__________________________________________________
"""
import logging
import time
import urllib.parse
import allure
import pytest
import string
import random
from random import randint
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class BasePageClass:
    EXIT_PATH_URL = ""
    _timeout = 50
    _COMPANY_LOGO_LOCATOR = (By.CSS_SELECTOR, "img.header-logo")
    _ALL_CDN_SCRIPT_LOGOS_LOCATOR = (By.CSS_SELECTOR, "script[src]")
    _FOCUS_TAG_LOCATOR = (By.CSS_SELECTOR, "body")
    _LOCATOR = (By.CSS_SELECTOR, 'div[class*="row"]')
    _LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'a[href^="/login/"]')
    _LEADING_MODAL_CLOSE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button.leadinModal-close")
    _SOUNDS_GOOD_BUTN_LOCATOR = (
        By.XPATH,
        "/html/body/div[1]/div/a",
    )
    _LANDING_PAGE_SOUNDS_GOOD_BUTN_LOCATOR = (
        By.CSS_SELECTOR,
        "body > div:nth-child(1) div a",
    )
    _SELECT_LANGUAGE_OPTION = (By.ID, "locale-select")
    _SELECT_LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, "#locale-select option")
    _WINDOW_SELECT_LOCATOR = (By.TAG_NAME, 'body')

    def __init__(self, *args):
        self.selenium = args[0]
        self.client = pytest.current_client

    def check_page_url(self, check_url, path=None):
        logging.debug("URl is = ", check_url)
        url = urllib.parse.urljoin(check_url, path)
        return self.check_for_new_url(url)

    @allure.step("Go to link is {link}")
    def go_to_page(self, link):
        """Instructs webdriver make a GET request to the page URL.
        This method is blocking until the entire page loads.
        """
        return self.selenium.get(link)

    def refresh(self):
        self.selenium.refresh()

    def maximize(self):
        self.selenium.maximize_window()

    def go_to(self, path):
        self.selenium.get(path)

    def get_current_url(
            self,
    ):
        url = self.selenium.current_url
        logging.debug(url)
        return url

    def click_on_element(self, locator=None, index=None):
        """Generic function for clicking elements. (Range index version)"""
        click_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.selenium, self._timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button_link = self.selenium.find_elements(*locator)
            if index is None:
                if len(button_link) > 1:
                    index = randint(0, len(button_link) - 1)
                else:
                    index = 0
            self.wait_it_out(0.5)
            self.get_text_of_elements()
            button_link[index].click()
            click_result = True
            return click_result
        finally:
            pass

    def click_on_single_element(self, locator=None):
        """Generic function for clicking elements. (Range index version)"""
        click_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.selenium, self._timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button_link = self.selenium.find_element(*locator)
            self.wait_it_out(0.5)
            self.get_text_of_elements()
            button_link.click()
            click_result = True
            return click_result
        finally:
            pass

    def check_for_new_url(
            self, expected_url_string=EXIT_PATH_URL, interval=0.5, max_limit=_timeout
    ):
        """Generic Method to check until a new url is loaded, at given interval (in seconds)"""
        check_result = False
        cycle = 0.0
        max_limit = float(max_limit)
        try:
            while check_result is False and expected_url_string is not None:
                self.wait_it_out(interval)
                cycle += interval
                current_page_url = str(self.selenium.current_url)
                if expected_url_string in current_page_url:
                    check_result = True
                    self.wait_it_out(1)
                    return check_result
                if cycle > max_limit:
                    logging.debug("\n We want URL : ", expected_url_string)
                    logging.debug("\n We are now at URL : ", current_page_url)
                    return check_result
        finally:
            logging.debug(check_result)

    def get_text_of_elements(self, locator=_FOCUS_TAG_LOCATOR):
        """Returns list of text of element/s"""
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator)
        )
        WebDriverWait(self.selenium, self._timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.wait_it_out(0.5)
        element = self.selenium.find_elements(*locator)
        if element is not None:
            element_texts = [elem.text for elem in element]

            return element_texts

    def convert_list_to_string(self, list):
        return "".join(list)

    @classmethod
    def wait_it_out(cls, seconds=1.0):
        time.sleep(seconds)
        return True

    def enter_field_input(
            self, input_locator=_FOCUS_TAG_LOCATOR, values="No Input", index=None
    ):
        """Generic Input function to enter passed values into field element"""
        fill_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(input_locator)
            )  # Present?
            WebDriverWait(self.selenium, self._timeout).until(
                EC.visibility_of_element_located(input_locator)
            )  # Visible?
            name_field = self.selenium.find_elements(*input_locator)
            if index is None:
                if len(name_field) > 1:
                    index = randint(0, len(name_field) - 1)
                else:
                    index = 0
            self.wait_it_out(0.9)
            name_field[index].send_keys(Keys.CONTROL + "a")
            name_field[index].send_keys(Keys.BACKSPACE)
            name_field[index].send_keys(str(values))
            fill_result = True
            return fill_result
        except AssertionError as e:
            logging.debug("\n Got exception, which is apparently : ")
            logging.debug("\n", e)
        finally:
            logging.debug(fill_result)
        return fill_result

    def check_new_page(
            self, np_link_locator=None, required_string=None, index=None
    ):
        """Check if the Linked Page opens up in a New Tab"""
        check_result = False
        try:
            time.sleep(0.5)
            self.click_on_element(np_link_locator, index)
            self.selenium.switch_to.window(self.selenium.window_handles[1])
            self.maximize()
            if self.check_for_new_url(required_string, interval=1):
                check_result = True
            else:
                check_result = False
            return check_result
        finally:
            print(check_result)

    def check_fields_blank_error_message(self, locator, error_string):
        error = self.get_text_of_elements(locator)
        print(error)
        print(error_string)
        logging.debug("error_text", error)
        logging.debug(self.convert_list_to_string(error))
        res1 = self.convert_list_to_string(error) == error_string
        return res1

    def get_attribute_of_elements(
            self, locator=_FOCUS_TAG_LOCATOR, attribute_name="class"
    ):
        """Specialized function for getting attribute of elements."""
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator)
        )
        elements = self.selenium.find_elements(*locator)
        element_attributes = [elem.get_attribute(attribute_name) for elem in elements]
        return element_attributes

    def send_enter_keys_to_element(self, locator=None, index=None):
        """Specialized function for clicking elements. (Range index Enter version)"""
        click_result = False
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.selenium, self._timeout).until(
                EC.visibility_of_element_located(locator)
            )
            button_link = self.selenium.find_elements(*locator)
            if index is None:
                if len(button_link) > 1:
                    index = randint(0, len(button_link) - 1)
                else:
                    index = 0
            button_link[index].send_keys(Keys.ENTER)
            click_result = True
            return click_result
        finally:
            logging.debug(click_result)

    def click_on_browser_back_button(self):
        self.selenium.back()

    def check_same_page_link_works(
            self,
            sp_link_locator=None,
            required_string="https://masaischool.com",
            index=None,
    ):
        """Check if the Linked Page opens up in the Same Tab"""
        check_result = False
        try:
            self.wait_it_out(3)
            self.click_on_element(sp_link_locator, index)
            self.selenium.switch_to.window(self.selenium.current_window_handle)
            self.wait_it_out(5)
            check_result = bool(self.check_for_new_url(required_string, interval=2))
            self.click_on_browser_back_button()
            return check_result
        finally:
            logging.debug(check_result)

    def check_new_page_link_works(
            self, np_link_locator=None, required_string=None, index=None
    ):
        """Check if the Linked Page opens up in a New Tab"""
        check_result = False
        try:
            self.wait_it_out(0.5)
            self.click_on_element(np_link_locator, index)
            self.selenium.switch_to.window(self.selenium.window_handles[1])
            self.maximize()
            if self.check_for_new_url(required_string, interval=2):
                check_result = True
                self.selenium.close()
                self.selenium.switch_to.window(self.selenium.window_handles[0])
        finally:
            pass

    def check_element_is_clickable(self, locator=None, index=None):
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.selenium, self._timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button_link = self.selenium.find_elements(*locator)
            if index is None:
                if len(button_link) > 1:
                    return True
                else:
                    return False
            self.wait_it_out(0.5)
            click_result = True
            return click_result
        finally:
            pass

    def scroll_into_view(self, locator, index=0, scroll_val=150):
        self.check_page_element(locator, timeout=25)
        self.wait_it_out(1)
        elem = self.selenium.find_elements(*locator)
        if index is None:
            index = self.select_random_index(locator)
        self.selenium.execute_script(
            "return arguments[0].scrollIntoView();", elem[index]
        )
        self.selenium.execute_script("window.scrollBy(0, -" + str(scroll_val) + ");")

    def select_random_index(self, card_locator=_FOCUS_TAG_LOCATOR):
        card_list = self.get_page_elements(card_locator)
        self.wait_it_out(1)
        card_count = len(card_list)
        if card_count > 1:
            index = randint(0, card_count - 1)
        else:
            index = 0
        return index

    def get_page_elements(self, locator=_FOCUS_TAG_LOCATOR):
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator)
        )
        self.wait_it_out(2)
        web_elements = self.selenium.find_elements(*locator)
        return web_elements

    def switch_to_new_window(self, wait_quantum=1, timeout=10):
        check_result = False
        window_count = 0
        window_wait = 0
        try:
            while window_count < 2 or window_wait == timeout:
                self.wait_it_out(wait_quantum)
                window_wait += wait_quantum
                window_count = len(self.selenium.window_handles)
            if window_wait >= timeout:
                check_result = False
            else:
                self.selenium.switch_to.window(self.selenium.window_handles[1])
                check_result = True
        except AssertionError as exp:
            print("\n\nException : ", exp)
            return check_result
        return check_result

    def switch_to_old_window(self):
        check_result = False
        try:
            before_count = len(self.selenium.window_handles)
            self.selenium.close()
            self.wait_it_out(3)
            self.selenium.switch_to.window(self.selenium.window_handles[0])
            after_count = len(self.selenium.window_handles)
            check_result = bool(before_count > after_count)
            return check_result
        except AssertionError as exp:
            print("\n\nException : ", exp)
            return check_result

    def check_page_element(self, locator=_LOCATOR, timeout=None):
        """Check to see if given WebElement is in place, present and visible"""
        check_result = False
        try:
            if timeout is None:
                timeout = self._timeout
            WebDriverWait(self.selenium, timeout).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.selenium, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.wait_it_out(3)
            element = self.selenium.find_element(*locator)
            if element is not None:
                if element.tag_name is not None:
                    if element.text is not None:
                        check_result = True
                        return check_result
            return check_result
        finally:
            return check_result

    def get_length_of_element(self, locator=None):
        """Generic function to get the count of occurrence of an element"""
        try:
            WebDriverWait(self.selenium, self._timeout).until(
                EC.presence_of_element_located(locator)
            )
            button_link = self.selenium.find_elements(*locator)
            length_of_element = len(button_link)
            return length_of_element
        except Exception as e:
            print(e)

    def scroll_to_down(self):
        self.selenium.find_element(By.TAG_NAME, "body").send_keys(
            Keys.CONTROL + Keys.END)

    def scroll_to_top(self):
        self.selenium.find_element(By.TAG_NAME, "body").send_keys(
            Keys.CONTROL + Keys.HOME)

    def close_one_given_window(self, number):
        handles = list(self.selenium.window_handles)
        self.wait_it_out(1)
        self.selenium.switch_to.window(handles[int(number)])
        self.selenium.close()

    def close_current_page(self):
        self.selenium.close()
        return self.selenium.switch_to.window(self.selenium.window_handles[0])

    def check_new_window_link_works(
        self, nw_link_locator=None, required_string="masaischool", index=None
    ):
        """Check if the Linked Page opens up in a New window"""
        check_result = False
        try:
            # assert self.is_current_page
            time.sleep(0.5)
            if index is None:
                index = self.select_random_index(nw_link_locator)
            time.sleep(3)
            self.click_on_element(nw_link_locator, index)
            self.selenium.switch_to.window(self.selenium.window_handles[1])
            time.sleep(2)
            # print(self.selenium.current_url)
            if self.check_for_new_url(required_string, interval=2):
                self.wait_it_out(1)
                check_result = True
            else:
                check_result = False
            self.selenium.close()
            self.selenium.switch_to.window(self.selenium.window_handles[0])
            return check_result
        except AssertionError as exception_case:
            logging.debug("\nException : ", exception_case)

    def click_on_action_button(self):  # Open action modal
        self.wait_it_out(5)
        hover_ele = self.selenium.find_element(By.CSS_SELECTOR, "div .has-action-button")
        action = ActionChains(self.selenium)
        action.move_to_element(hover_ele).perform()
        action.click(hover_ele)
        action_button = self.selenium.find_element(By.CSS_SELECTOR,
                                                   "#ptable_actions >.mat-button-wrapper")
        action.move_to_element(action_button).perform()
        action_button.click()
        self.wait_it_out(2)
        return True

    def get_the_status_code_for_current_link(self, current_link):
        print("Status code for the link is = ", requests.get(current_link).status_code)
        return requests.get(current_link)

    def select_value_from_list(self, locator=None, index=None):
        """Generic function for selecting value. (Range index version)"""
        click_result = False
        WebDriverWait(self.selenium, self._timeout).until(
            EC.presence_of_element_located(locator)
        )
        WebDriverWait(self.selenium, self._timeout).until(
            EC.element_to_be_clickable(locator)
        )
        button_link = self.selenium.find_elements(*locator)
        if index is None:
            if len(button_link) > 1:
                index = randint(0, len(button_link) - 1)
            else:
                index = 0
        self.wait_it_out(0.5)
        self.get_text_of_elements()
        element = Select(self.selenium.find_element(*locator))
        time.sleep(0.8)
        element.select_by_index(index)
        click_result = True
        return click_result

    @staticmethod
    def generate_string(i):
        return ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=i))