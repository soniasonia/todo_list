from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
from list_app.forms import EMPTY_LIST_ERROR, DUPLICATE_ERROR


class ItemValidationTest(FunctionalTest):
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        elem = self.get_item_input_box()
        elem.send_keys(' \n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        elem = self.get_item_input_box()
        elem.send_keys('a')
        self.assertFalse(error.is_displayed())

    def test_cannot_add_empty_list_items(self):
        # Edyta próbuje dodać pusty element
        self.browser.get(self.live_server_url)
        elem = self.get_item_input_box()
        elem.send_keys(' \n')
        # Pojawia się komunikat błędu, że nie można dodać pustego elementu
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_LIST_ERROR)

        # Edyta próbuje dodać normalny element
        elem = self.get_item_input_box()
        elem.send_keys('Kupić mleko\n')
        self.check_for_row_in_list('1: Kupić mleko')

        # nie da się dodać pustego elementu (druga próba)
        elem = self.get_item_input_box()
        elem.send_keys(' \n')
        self.check_for_row_in_list('1: Kupić mleko')
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_LIST_ERROR)

        #Edyta dodaje jeszcze jeden element
        elem = self.get_item_input_box()
        elem.send_keys('Zrobić herbatę\n')
        self.check_for_row_in_list('1: Kupić mleko')
        self.check_for_row_in_list('2: Zrobić herbatę')

    def test_list_item_validation(self):
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Kupić kalosze\n')
        self.check_for_row_in_list('1: Kupić kalosze')
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Kupić kalosze\n')
        self.check_for_row_in_list('1: Kupić kalosze')
        error = self.get_error_element()
        self.assertEqual(error.text, DUPLICATE_ERROR)
