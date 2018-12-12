import pytest
from selenium import webdriver
import re
import time

@pytest.fixture(scope="class")
def setup(request):
    print("initiating edge driver")
    driver = webdriver.Edge()
    request.cls.driver = driver
    driver.get("http://localhost/litecart/")
    driver.maximize_window()
    yield driver
    driver.close()

# приводим к единому виду ответы браузеров о цвете элемента
def rgb_to_list(color):
    regex = r"\((.*?)\)"
    m = re.search(regex, color)
    colors = m.group(1)
    return colors.replace(" ", "").split(',')

@pytest.mark.usefixtures("setup")
class TestPage:

    def test_page(self):
        #сначала находим элемент из раздела Campaigns и получаем его свойства
        mains = self.driver.find_elements_by_css_selector('div#box-campaigns li.product')
        if mains:
            m = mains[0]
        main_text = m.find_element_by_css_selector('div.name').text
        m_reg_price = m.find_element_by_css_selector('.regular-price')
        m_camp_price = m.find_element_by_css_selector('.campaign-price')
        main_regular_price = m_reg_price.text
        main_campaign_price = m_camp_price.text
        main_regular_price_tag = m_reg_price.tag_name
        main_campaign_price_tag = m_camp_price.tag_name
        main_regular_price_color = m_reg_price.value_of_css_property(
            'color')
        main_regular_price_color = rgb_to_list(main_regular_price_color)
        main_campaign_price_color = m_camp_price.value_of_css_property(
            'color')
        main_campaign_price_color = rgb_to_list(main_campaign_price_color)
        main_regular_price_size = m_reg_price.value_of_css_property('font-size')
        main_regular_price_size = float(main_regular_price_size[:-2])
        main_campaign_price_size = m_camp_price.value_of_css_property(
            'font-size')
        main_campaign_price_size =  float(main_campaign_price_size[:-2])

        #переходим на страницу товара
        m.find_element_by_css_selector('a').click()
        time.sleep(3)                                                               #без ожидания не работало под Edge
        p = self.driver.find_element_by_css_selector('div#box-product')             #карточка товара. относительно нее будем строить локаторы
        product_text = p.find_element_by_css_selector('h1').text
        p_reg_price = p.find_element_by_css_selector('.regular-price')
        p_camp_price = p.find_element_by_css_selector('.campaign-price')
        product_regular_price = p_reg_price.text
        product_campaign_price = p_camp_price.text
        product_regular_price_tag = p_reg_price.tag_name
        product_campaign_price_tag = p_camp_price.tag_name
        product_regular_price_color = p_reg_price.value_of_css_property(
            'color')
        product_regular_price_color = rgb_to_list(product_regular_price_color)
        product_campaign_price_color = p_camp_price.value_of_css_property(
            'color')
        product_campaign_price_color = rgb_to_list(product_campaign_price_color)
        product_regular_price_size = p_reg_price.value_of_css_property('font-size')
        product_regular_price_size = float(product_regular_price_size[:-2])
        product_campaign_price_size = p_camp_price.value_of_css_property(
            'font-size')
        product_campaign_price_size = float(product_campaign_price_size[:-2])

        #выполняем требуемые проверки

        assert main_text == product_text
        assert main_regular_price == product_regular_price
        assert main_campaign_price == product_campaign_price
        assert main_regular_price_tag == 's'
        assert main_regular_price_color[0] == main_regular_price_color[1] == main_regular_price_color[2]
        assert main_campaign_price_tag == 'strong'
        assert int(main_campaign_price_color[1]) == int(main_campaign_price_color[2]) == 0
        assert product_regular_price_tag == 's'
        assert product_regular_price_color[0] == product_regular_price_color[1] == product_regular_price_color[2]
        assert product_campaign_price_tag == 'strong'
        assert int(product_campaign_price_color[1]) == int(product_campaign_price_color[2]) == 0
        assert main_campaign_price_size > main_regular_price_size
        assert product_campaign_price_size > product_regular_price_size



