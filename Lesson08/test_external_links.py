import pytest
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# проверено в Firefox, Chrome, Edge

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Edge()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/admin")
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestExternalLinks:
    def test_login(self):
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_name('login').click()

    def test_there_and_back_again(self):
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Countries')]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text('Andorra').click()
        time.sleep(1)
        main_window = self.driver.current_window_handle
        old_windows = self.driver.window_handles
        for link in self.driver.find_elements_by_css_selector('.fa-external-link'):
            link.click()
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.new_window_is_opened(old_windows))
            new_windows = self.driver.window_handles
            second_window = (set(new_windows) - set(old_windows)).pop()
            assert second_window
            time.sleep(1)
            self.driver.switch_to.window(second_window)
            self.driver.close()
            self.driver.switch_to.window(main_window)


