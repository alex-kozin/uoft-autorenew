from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get("file:///D:/Users/alexa/Desktop/one_renewed_one_fails.html")

    # Get the results of the renewal attempt
    status_log = driver.find_elements(By.XPATH, "//div[@class='content']/h3")
    assert 1 <= len(status_log) <= 2
    for status_entry in status_log:
        message = status_entry.text
        print(f"Status: {message}")
        print(f"Items: {message.split(' ', 1)[0]}\n===============")

    items_log = driver.find_elements(By.XPATH, "//div[@class='defaultstyle']/dl")
    for item_entry in items_log:
        message = item_entry.find_element(By.XPATH, ".//dt").text
        item_info = item_entry.find_element(By.XPATH, ".//dd").text
        print(f"Result: {message}")
        print(f"Item:\n{item_info}\n===============")
