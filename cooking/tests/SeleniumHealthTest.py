import os
import selenium
from selenium.common.exceptions import NoSuchElementException
from concurent_cooking.settings import BASE_DIR
from datetime import date
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import ugettext as _
from cooking.tests import util

__author__ = 'sarace'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SeleniumHealtTest(StaticLiveServerTestCase):
    SCREEN_SHOT_FOLDER = os.path.join(BASE_DIR, "selenium_ide_test_cases/sceenshots")
    FIREFOX_PROFILE_PATH = os.path.expanduser("~/.mozilla/firefox/o1igxqtg.default")

    def take_screen_shot(self, name):
        today = date.today().strftime("%d_%m_%y")
        screenshot_name = ''.join([name, '_', today, '.png'])
        self.selenium.save_screenshot(os.path.join(self.SCREEN_SHOT_FOLDER, screenshot_name))


    def getUrl(self, url):
        self.selenium.get('%s%s' % (self.live_server_url, url))

    def is_element_present(self,id):
        """
        Check if an element is present on a web page.
        :param id:
        :return:
        """
        try:
            self.selenium.find_element_by_id(id)
        except NoSuchElementException:
            return False
        return True

    @classmethod
    def setUpClass(cls):
        """
        Initialisation for all the testCase , done only once
        - Initialise Firefox driver
        - Maximize browser window
        :param cls:
        :return:
        """
        profile = webdriver.FirefoxProfile(cls.FIREFOX_PROFILE_PATH)
        cls.selenium = webdriver.Firefox(profile)
        cls.selenium.implicitly_wait(10)
        cls.selenium.maximize_window()
        super(SeleniumHealtTest, cls).setUpClass()

    def setUp(self):
        """
        Initialisation For each test:

        :return:
        """
        self.verificationErrors = []

    @classmethod
    def tearDownClass(cls):
        """
        - close selenium conexion
        :return:
        """
        cls.selenium.quit()
        super(SeleniumHealtTest, cls).tearDownClass()

    def test_connexion_page(self):
        """
        Test the opening of the connexion page
        :return:
        """
        self.getUrl("/")
        assert "Concurent Cooking" in self.selenium.title
        assert self.selenium.find_element_by_id('userId') is not None
        assert self.selenium.find_element_by_id('passwordId') is not None
        self.take_screen_shot('connexion_page')

    def test_invalid_login(self):
        """
        Test the opening of the connexion page
        :return:
        """
        self.getUrl("/")
        assert "Concurent Cooking" in self.selenium.title

        user_name_field = self.selenium.find_element_by_id('userId')
        user_name_field.send_keys('InvalidUsername')
        user_password_field = self.selenium.find_element_by_id('passwordId')
        user_password_field.send_keys('InvalidPassword')
        login_button = self.selenium.find_element_by_id('login_btn')
        login_button.click()
        error_message = self.selenium.find_element_by_id('error_message')
        assert error_message is not None
        assert error_message.text == _('Invalid user or password')
        self.take_screen_shot('invalid_login')

    def test_valid_non_admin_login(self):
        """
        Test the opening of the connexion page
        :return:
        """
        self.getUrl("/")
        assert "Concurent Cooking" in self.selenium.title

        util.initTestUser()

        user_name_field = self.selenium.find_element_by_id('userId')
        user_name_field.send_keys('test_user')
        user_password_field = self.selenium.find_element_by_id('passwordId')
        user_password_field.send_keys('test_password')
        login_button = self.selenium.find_element_by_id('login_btn')
        login_button.click()
        logout_btn = self.selenium.find_element_by_id('logout_btn')
        self.assertTrue(self.is_element_present('logout_btn'))
        assert self.is_element_present('cooking_link')
        assert self.is_element_present('it_link')
        self.assertFalse(self.is_element_present('admin_link'))
        self.take_screen_shot('valid__non_admin_login')
