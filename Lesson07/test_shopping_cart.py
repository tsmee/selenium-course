import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# проверено в Firefox, Chrome, Edge

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    request.cls.driver = driver
    driver.get("http://localhost/litecart")
    driver.maximize_window()
    yield driver
    driver.close()

@pytest.mark.usefixtures("setup")
class TestProductCart:
    def test_adding_products(self):
        while int(self.driver.find_element_by_css_selector('span.quantity').text) < 3:
            self.driver.find_element_by_css_selector('li.product a.link').click()
            quantity = int(self.driver.find_element_by_css_selector('span.quantity').text)
            print(quantity)
            size = self.driver.find_elements_by_name("options[Size]")
            if size:
                Select(size[0]).select_by_index(2)
            self.driver.find_element_by_name('add_cart_product').click()
            wait = WebDriverWait(self.driver, 10)  # seconds
            wait.until(EC.text_to_be_present_in_element((By.XPATH, "//span[@class='quantity']"), str(quantity + 1)))
            print("changed successfully")
            self.driver.find_element_by_css_selector('div#logotype-wrapper a').click()
        assert int(self.driver.find_element_by_css_selector('span.quantity').text) == 3

    def test_delete_products(self):ё
        self.driver.find_element_by_link_text('Checkout »').click()
        while self.driver.find_elements_by_css_selector('td.item'):
            element = self.driver.find_element_by_css_selector('td.item')
            self.driver.find_element_by_name("remove_cart_item").click()
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.staleness_of(element))
        assert self.driver.find_element_by_xpath('//em').text == 'There are no items in your cart.'
