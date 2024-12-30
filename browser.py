import random
import time
from logger_module import logger
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import \
    LOGIN_PAGE_URL, PASSWORD_CSS_SELECTOR, LOGIN_CSS_SELECTOR, SIGNIN_BUTTON_CSS_SELECTOR, \
    CAPTCHA_URL, PROFILE_PAGE_URL, PROFILE_IMAGE_CSS_SELECTOR


class Browser:

    def __init__(self, login: str, password: str):
        try:
            self.driver = webdriver.Chrome()
            self.login(login, password)
            self.parse_profile_image()
        finally:
            self.driver.quit()

    def login(self, login, password):
        """
            Open login page, fill login,password inputs
            Press Login Button, wait for captcha resolve

            :param str login: Email/phone number
            :param str password: Password
        """
        self.open_page(LOGIN_PAGE_URL)
        login_input = self.find_element(By.CSS_SELECTOR, LOGIN_CSS_SELECTOR)
        password_input = self.find_element(By.CSS_SELECTOR, PASSWORD_CSS_SELECTOR)
        submit_button = self.find_element(By.CSS_SELECTOR, SIGNIN_BUTTON_CSS_SELECTOR)

        if not login_input or not password_input:
            logger.error('Input not found')
            return

        login_input.send_keys(login)
        self.__random_sleep()  # sleep between 1 and 3 seconds
        password_input.send_keys(password)

        submit_button.click()
        self.__random_sleep()  # sleep between 1 and 3 seconds

        if CAPTCHA_URL in self.driver.current_url:
            logger.warning('Captcha page obtained! Please fill captcha and press Enter')
            input()
            self.__random_sleep()

    def parse_profile_image(self):
        """
            Open profile page, find profile image
        """
        self.open_page(PROFILE_PAGE_URL)
        self.__random_sleep()
        profile_svg_element = self.wait_for_element(By.CSS_SELECTOR, PROFILE_IMAGE_CSS_SELECTOR)
        if profile_svg_element:
            profile_image_element = profile_svg_element.find_element(By.CSS_SELECTOR, 'image')
            logger.info('Profile Image Link: %s' % profile_image_element.get_attribute('xlink:href'))
        else:
            logger.error('Profile Image not found')

    def open_page(self, page_url):
        """
            Open page and wait until page body loaded
            :param str page_url: Page URL to open
        """
        self.driver.get(page_url)
        self.wait_for_element(By.TAG_NAME, "body")
        logger.debug('Page %s loaded' % page_url)

    def wait_for_element(self, by, value):
        """
            Wait for element

            :param str by: Search type ( XPath / CSS / etc. )
            :param str value: Searchable value
            :return: Element / None
            :rtype: WebElement
        """
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        except Exception:
            logger.error('Element %s not found' % value)

    def find_element(self, by, value):
        """
            Find element

            :param str by: Search type ( XPath / CSS / etc. )
            :param str value: Searchable value
            :return: Element / None
            :rtype: WebElement
        """
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            logger.error('Element %s not found' % value)

    @staticmethod
    def __random_sleep():
        """
            Random sleep from 1 to 3
        """
        random_time = random.randrange(1, 3)
        time.sleep(random_time)
