from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def SetUpClass(cls):
        pass

    @classmethod
    def TearDownClass(cls):
        pass

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # To skip warnings that happen in Windows
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list(self, text):
        pass

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')