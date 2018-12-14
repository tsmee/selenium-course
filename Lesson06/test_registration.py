import pytest
from selenium import webdriver
from random import choice
import string
import time

# проверено в Firefox, Chrome, Edge

def generate_email():
    return ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(10)) + '@hotmail.com'

@pytest.fixture(scope="class")
def setup(request):
    print("initiating driver")
    driver = webdriver.Edge()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/")
    driver.maximize_window()
    request.cls.email = generate_email()
    request.cls.password = '111111'
    yield driver
    driver.close()

@pytest.mark.usefixtures("setup")
class TestRegistration:
    def test_registration(self):
        print(self.email)
        self.driver.find_element_by_link_text('New customers click here').click()
        time.sleep(1)
        self.driver.find_element_by_name('firstname').send_keys('Bernard')
        self.driver.find_element_by_name('lastname').send_keys('Black')
        self.driver.find_element_by_name('address1').send_keys('Elm street 27')
        self.driver.find_element_by_name('city').send_keys('Raccoon City')
        country = self.driver.find_element_by_name('country_code')
        self.driver.execute_script("arguments[0].selectedIndex = 224; arguments[0].dispatchEvent(new Event('change'))",
                                   country)
        time.sleep(1)
        hiddenselect = self.driver.find_element_by_xpath(('//select[@name="zone_code"]'))
        self.driver.execute_script("arguments[0].selectedIndex = 22; arguments[0].dispatchEvent(new Event('change'))", hiddenselect)
        self.driver.find_element_by_name('postcode').send_keys('32167')
        self.driver.find_element_by_name('phone').send_keys('23423423')
        self.driver.find_element_by_name('email').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('confirmed_password').send_keys(self.password)
        self.driver.find_element_by_name('create_account').click()


    def test_logout(self):
        time.sleep(2)
        self.driver.find_element_by_link_text('Logout').click()

    def test_login(self):
        time.sleep(2)
        self.driver.find_element_by_name('email').send_keys(self.email)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_name('login').click()

    def test_logout_again(self):
        time.sleep(2)
        self.driver.find_element_by_link_text('Logout').click()
