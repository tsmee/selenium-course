import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Firefox()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestGeozones:
    def test_login(self):
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_name('login').click()

    def test_geozones(self):
        geozone_links = []
        country_rows = self.driver.find_elements_by_xpath("//tr[@class='row']/td[3]/a")
        for n in country_rows:
            geozone_links.append(n.get_attribute("href"))
            print(n.get_attribute("href"))
            print(len(geozone_links))
        for link in geozone_links:
            self.driver.get(link)
            geozones_unsorted = []
            geozones = self.driver.find_elements_by_xpath("//*[contains(@name,'[zone_code]')]/option[@selected='selected']")
            for n in geozones:
                geozones_unsorted.append(n.text)
            assert sorted(geozones_unsorted) == geozones_unsorted
            current_country = self.driver.find_element_by_xpath("//input[@name='name']").get_attribute('value')
            print('Country: '+ current_country + '. Zones are in correct order.')
`

