from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta
        self.browser.get(self.live_server_url)
        # self.browser.get('http://localhost:8000')
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Utwórz nową listę', header_text)
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Wpisz rzecz do zrobienia')
        inputbox.send_keys('Kupić pawie pióra')
        inputbox.send_keys(Keys.ENTER)
        test_list_url = self.browser.current_url
        self.assertRegex(test_list_url, '/lists/.+')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Kupić pawie pióra', [row.text for row in rows])

        # Janek
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Kupić pawie pióra', page_text)

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)
        test_second_list_url = self.browser.current_url
        self.assertRegex(test_second_list_url, '/lists/.+')
        self.assertNotEqual(test_list_url, test_second_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Kupić pawie pióra', page_text)
        self.assertIn('1: Kupić mleko', page_text)
