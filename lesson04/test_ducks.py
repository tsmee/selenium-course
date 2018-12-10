import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Firefox()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/")
    driver.maximize_window()
    # yield driver
    # driver.close()


@pytest.mark.usefixtures("setup")
class TestDucks:
    def test_ducks(self):
        ducks = self.driver.find_elements_by_css_selector("li.product")
        for n in ducks:
            assert len(n.find_elements_by_xpath(".//div[contains(@class,'sticker')]")) == 1
            sticker_text = n.find_element_by_xpath(".//div[contains(@class,'sticker')]").text
            ducks_name = n.find_element_by_xpath(".//div[@class='name']").text
            print(ducks_name + "'s " "sticker type is " + sticker_text)

