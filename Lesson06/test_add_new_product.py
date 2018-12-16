import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from os import getcwd
from time import sleep

# проверено в Firefox, Chrome, Edge

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/admin")
    driver.maximize_window()
    yield driver
    driver.close()

@pytest.mark.usefixtures("setup")
class TestAddingProduct:
    def test_login(self):
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_name('login').click()

    def test_add_new_product(self):
        sleep(1)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Catalog')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Add New Product')]").click()
        sleep(2)
        self.driver.find_element_by_css_selector("input[type='radio'][value='1']").click()          #status = enabled
        self.driver.find_element_by_xpath("//input[@name='name[en]']").send_keys('Python Duck')
        self.driver.find_element_by_xpath("//input[@name='code']").send_keys('rd2018')
        self.driver.find_element_by_xpath("//input[@name='categories[]' and @data-name='Rubber Ducks']").click()
        default_category = self.driver.find_element_by_name('default_category_id')
        Select(default_category).select_by_visible_text('Rubber Ducks')
        self.driver.find_element_by_xpath("//input[@name='product_groups[]' and @value='1-3']").click()
        self.driver.find_element_by_xpath("//input[@name='quantity']").send_keys(Keys.HOME)
        self.driver.find_element_by_xpath("//input[@name='quantity']").send_keys("10")
        upload = self.driver.find_element_by_xpath("//input[@name='new_images[]']")
        upload.send_keys(getcwd()+"\duck.png")
        sleep(2)


        self.driver.find_element_by_link_text('Information').click()
        manufacturer = self.driver.find_element_by_name('manufacturer_id')
        Select(manufacturer).select_by_index(1)
        self.driver.find_element_by_name('keywords').send_keys('duck, python')
        self.driver.find_element_by_class_name('trumbowyg-editor').send_keys('Awesome present for your friend who likes Python and rubber ducks. '
                                                                             'About 3.5 inches long with the cape measuring about 4.5 inches.')
        sleep(2)

        self.driver.find_element_by_link_text('Prices').click()
        self.driver.find_element_by_name('purchase_price').send_keys('10')
        currency = self.driver.find_element_by_name('purchase_price_currency_code')
        Select(currency).select_by_index(1)
        self.driver.find_element_by_name('prices[USD]').send_keys('200')
        sleep(2)

        self.driver.find_element_by_xpath("//button[@name='save']").click()

    def test_new_product(self):
        sleep(1)
        new_duck = self.driver.find_elements_by_link_text('Python Duck')
        assert new_duck
