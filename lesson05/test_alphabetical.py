import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Firefox()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestAlphabetical:

    def test_title(self):
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_name('login').click()

    def test_alphabetical(self):
        countires_unsorted = []
        countries = self.driver.find_elements_by_xpath("//tbody/tr[@class='row']/td[5]")
        for n in countries:
            countires_unsorted.append(n.text)
        assert sorted(countires_unsorted) == countires_unsorted
        print('List of countries: Alphabetical order is correct.')

    def test_more_zones(self):
        countries = self.driver.find_elements_by_xpath("//tbody/tr[@class='row']")
        more_zones_urls = []
        for z in countries:
            if int(z.find_element_by_xpath('.//td[6]').text) > 0:
                more_zones_urls.append(z.find_element_by_xpath('.//td[5]/a').get_attribute('href'))
        print(len(more_zones_urls))
        for t in more_zones_urls:
            self.driver.get(t)
            zones_unsorted = []
            zones = self.driver.find_elements_by_xpath("//tbody/tr/td[3]/input")
            for n in zones:
                if n.get_attribute("value"):
                    zones_unsorted.append(n.get_attribute("value"))
            assert sorted(zones_unsorted) == zones_unsorted
            current_country = self.driver.find_element_by_xpath("//tbody//input[@name='name']").get_attribute("value")
            print('Current country: ' + current_country + '. Alphabetical order is correct')

