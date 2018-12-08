import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def setup(request):
    print("initiating chrome driver")
    driver = webdriver.Firefox()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/admin")
    driver.maximize_window()
    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestExample:

    def test_title(self):
        self.driver.find_element_by_name('username').send_keys('admin')
        self.driver.find_element_by_name('password').send_keys('admin')
        self.driver.find_element_by_name('login').click()

    def test_content_text(self):
        menu = self.driver.find_elements_by_xpath('//*[@id="app-"]')
        print('\n')
        for n in range(1, len(menu)+2):
            # проверяем, на каком мы пункте меню (категории). если пункт меню найден, проверяем наличие заголовка
            menu_title = self.driver.find_elements_by_xpath("//li[contains(@class,'selected')]/a/span[2]")
            if menu_title:
                current_menu = menu_title[0].text
                h1text = self.driver.find_elements_by_tag_name('h1')
                assert len(h1text) == 1
                print(current_menu + "<H1>" + h1text[0].text + "</H1>")
            path = """//*[@id="app-"][{n}]/a""".format(n=str(n))
            submenu = self.driver.find_elements_by_xpath("//li[contains(@class,'selected')]/ul/li")

            if len(submenu) > 0:
                for z in range(2, len(submenu) + 2):
                    # проверяем, на каком вложенном пункте меню находимся. если пункт меню найден, проверяем наличие заголовка
                    submenu_title = self.driver.find_elements_by_xpath("//li[contains(@class,'selected')]//li[contains(@class,'selected')]//span")
                    if submenu_title:
                        h1text = self.driver.find_elements_by_tag_name('h1')
                        assert len(h1text) == 1
                        print("..." + submenu_title[0].text + "<H1>" + h1text[0].text + "</H1>")
                    submenu_path = """//li[contains(@class,'selected')]/ul/li[{z}]""".format(z=str(z))
                    if z <= len(submenu):
                        self.driver.find_element_by_xpath(submenu_path).click()
            # проверяем страницу и заголовок после нажатия на последний пункт меню. ничего умнее не придумал,
            # selenium не позволяет ожидать загрузку страницы, которая должна открыться после клика на ссылку
            if n < 18:
                self.driver.find_element_by_xpath(path).click()
