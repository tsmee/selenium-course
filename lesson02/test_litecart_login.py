from selenium import webdriver
import pytest

@pytest.fixture
def driver(request):
    wd = webdriver.Firefox()
    # request.addfinalizer(wd.quit)
    return wd

def test_litecart_login(driver):
    driver.get('http://localhost/litecart/admin')
    driver.find_element_by_name('username').send_keys('admin')
    driver.find_element_by_name('password').send_keys('admin')
    driver.find_element_by_name('login').click()
    return driver

def test_find_menu_elements(driver):
    driver.find_element_by_id("app-")




