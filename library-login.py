from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def ajax_complete(driver):
    return 0 == driver.execute_script("return jQuery.active")


if __name__ == "__main__":

    base_url = "https://toroprod.library.utoronto.ca"
    options_url = "uhtbin/cgisirsi/x/x/0/1/488/X/BLASTOFF/"

    # Include the path to phantomjs.exe to your PATH environment variable
    driver = webdriver.PhantomJS()

    WebDriverWait(driver, 10).until(
        ajax_complete, "Timeout waiting for page to load")

    driver.find_element_by_class_name()

