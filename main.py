import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Custom Decorator Imports
from custom_decorators import (
    wait_for_element_to_be_clickable,
)  # Functions using this will need to accept "driver" and "clickable_element" as args


# TODO Add --Headless option and tests to validate the headless operation... cuzzzz headless will make it go way faster and will require less waits.

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(options=chrome_options)

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print(EMAIL)

# Open LinkedIn job page
linkedin_url = driver.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=4024184607&distance=25&f_AL=true&geoId=104116203&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
)

# FUUUUUUUUUUUCK I really want this decorator to work, but its being a pain in the dick. fuck it, whatever.
# @wait_for_element_to_be_clickable(By.LINK_TEXT, "Sign In")
# def sign_in(clickable_element):
#     driver.execute_script("arguments[0].click()", clickable_element)

# sign_in()


def init_sign_in():

    # Wait until the "Sign In" link is clickable and click it
    sign_in_link = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
    )
    driver.execute_script("arguments[0].click()", sign_in_link)
    # Add a small delay to let the modal load
    time.sleep(3)

    try:
        if EMAIL is None or PASSWORD is None:
            raise ValueError("EMAIL or PASSWORD is not set, check your .env file, foo.")

        driver.find_element(By.CSS_SELECTOR, "#username").send_keys(EMAIL)
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys(PASSWORD)
    except NoSuchElementException as error:
        raise NoSuchElementException(f"Cant find element. Details:: {str(error)}")

    secondary_sign_in = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#organic-div form div.login__form_action_container button",
            )
        )
    )
    driver.execute_script("arguments[0].click()", secondary_sign_in)


init_sign_in()


# driver.quit()
