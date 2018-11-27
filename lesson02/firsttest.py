from selenium import webdriver

def first_test():
    driver = webdriver.Firefox()
    driver.get('http://software-testing.ru/')
    driver.quit()

first_test()