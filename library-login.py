from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ajax_complete(driver):
    try:
        return "complete" == driver.execute_script("return document.readyState")
    except WebDriverException:
        pass


if __name__ == "__main__":

    base_url = "https://toroprod.library.utoronto.ca"
    options_url = "uhtbin/cgisirsi/x/x/0/1/488/X/BLASTOFF/"
    config = open("autorenew.config").readlines()
    argc = 4
    if len(config) != argc:
        print(f"Not enough arguments in config file, expected: {argc}")
        exit(1)

    login = config[0]
    pin = config[1]
    chrome_binary = config[2].rstrip()

    if config[3].isspace():
        print("No renewal options specified. Aborting...")
        exit(1)

    items_to_renew = {int(choice) for choice in config[3].split(" ")}

    options = Options()
    # TODO: Uncomment in production
    # options.add_argument('headless')
    if chrome_binary:
        options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    driver = webdriver.Chrome(options=options)

    driver.get(base_url + "/" + options_url)

    # All option elements are stored in a list with class "gatelist_table"
    table = driver.find_elements(By.XPATH, '//ul[@class="gatelist_table"]/li/a')

    links = {}
    for link_element in table:
        links[link_element.text] = str(link_element.get_attribute("href"))

    # Selecting materials renewal
    print("Going for option 1: Renew my materials")
    for description, link in links.items():
        if "materials" in description:
            driver.get(link)
            print("Found renew option.")
            break

    # input form with "new_session" name
    login_form = driver.find_element(By.NAME, "accessform")
    login_input = login_form.find_element(By.XPATH, "//input[@type='text' and @name='user_id']")
    pin_input = login_form.find_element(By.NAME, "password")

    submit_button = login_form.find_element(By.XPATH, '//ul/li[@class="submit-wrapper"]/input[@type="submit"]')

    driver.execute_script("arguments[0].value = arguments[1];", login_input, login)
    driver.execute_script("arguments[0].value = arguments[1];", pin_input, pin)
    submit_button.click()

    WebDriverWait(driver, 10).until(ajax_complete,
                                    "Timed out while waiting for the page to load")

    renew_form = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "renewitems")),
        "Timed out while waiting for the form to be located")

    # Querying data on materials
    materials = renew_form.find_elements(By.XPATH, '//table/tbody/tr')

    dates_data = driver.find_elements(By.XPATH, "//td[starts-with(@class, 'itemlisting') and @align='left']/strong")
    titles_data = driver.find_elements(By.XPATH, "//td[starts-with(@class, 'itemlisting')]/label")

    due_datetimes = []

    for element in dates_data:
        due_datetime = datetime.strptime(element.text, "%d/%m/%Y,%H:%M")
        due_datetimes.append(due_datetime)
        print(element.text)
        print(due_datetime)

    for element in titles_data:
        order = element.get_attribute("for")[-1]
        title, author = element.text.split("   ")
        print(f"{order[-1]}) {title} by: {author}")


    # If any items are scheduled for renewal - renew them
    if items_to_renew:

        # Renewing items specified in the config
        for choice in items_to_renew:
            print(f"The due date for item #{choice} is {due_datetimes[choice-1]}.")
            time_difference = due_datetimes[choice-1] - datetime.now()
            # if time_difference.days < 1:
            checkbox = driver.find_element(By.XPATH, f"//input[@id='RENEW{choice}']")
            driver.execute_script("arguments[0].checked = true;", checkbox)

            submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
            submit_button.click()

            # Get the results of the renewal attempt
            status_log = driver.find_elements(By.XPATH, "//div[@class='content']/h3")
            assert 1 <= len(status_log) <= 2
            for status_entry in status_log:
                message = status_entry.text
                print(f"Status: {message}")
                print(f"Items: {message.split(' ', 1)[0]}\n===============")

            # And get the results specifically for each item
            # TODO: create a unique identifier based on these strings, check if they are consistent
            # TODO: when does the api return the # of renewals left? Is it random or not?
            # TODO: update the due date from the result
            items_log = driver.find_elements(By.XPATH, "//div[@class='defaultstyle']/dl")
            assert len(items_log) == len(items_to_renew)
            for item_entry in items_log:
                message = item_entry.find_element(By.XPATH, ".//dt").text
                item_info = item_entry.find_element(By.XPATH, ".//dd").text
                print(f"Result: {message}")
                print(f"Item:\n{item_info}\n===============")

            # else:
            #     print("Waiting until the due date comes. Aborting...")
