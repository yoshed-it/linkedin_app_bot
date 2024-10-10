import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Wait until the "Sign In" link is clickable and click it
sign_in_link = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
)
driver.execute_script("arguments[0].click()", sign_in_link)
# Add a small delay to let the modal load
time.sleep(3)


username_input = driver.find_element(By.ID, "username").send_keys(EMAIL)
password_input = driver.find_element(By.ID, "password").send_keys(PASSWORD)
# secondary_sign_in = driver.find_element(
#     By.CSS_SELECTOR, "#organic-div form div.login__form_action_container button"
# )

secondary_sign_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#organic-div form div.login__form_action_container button")
    )
)
secondary_sign_in.click()


# time.sleep(5)

# driver.quit()
