import os
import time
import re
from bs4 import BeautifulSoup
from termcolor import colored
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from pprint import pprint


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--incognito")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print(EMAIL)


linkedin_home = "https://www.linkedin.com/home"
linkedin_jobs = "https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&geoId=104116203&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER"


# FUUUUUUUUUUUCK I really want this decorator to work, but its being a pain in the dick. fuck it, whatever.
# @wait_for_element_to_be_clickable(By.LINK_TEXT, "Sign In")
# def sign_in(clickable_element):
#     driver.execute_script("arguments[0].click()", clickable_element)

# sign_in()


def init_sign_in():
    while driver.current_url != linkedin_home:
        driver.get(linkedin_home)

        if driver.current_url == linkedin_home:
            try:
                sign_in_link = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
                )
                driver.execute_script("arguments[0].click()", sign_in_link)

                if EMAIL is None or PASSWORD is None:
                    raise ValueError(
                        "EMAIL or PASSWORD is not set, check your .env file, foo."
                    )

                driver.find_element(By.CSS_SELECTOR, "#username").send_keys(EMAIL)
                driver.find_element(By.CSS_SELECTOR, "#password").send_keys(PASSWORD)

                secondary_sign_in = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            "#organic-div form div.login__form_action_container button",
                        )
                    )
                )
                driver.execute_script("arguments[0].click()", secondary_sign_in)
                return

            except NoSuchElementException as error:
                raise NoSuchElementException(
                    f"Cant find element. Details: {str(error)}"
                )
            except Exception as error:
                print(f"Error during sign-in {error}")
                return


def validate_home():
    try:
        validate_logged_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#global-nav div nav ul li:nth-child(3) a span",
                )  # Checks for a unique element located only on the feed page.
            )
        )
        if validate_logged_in:
            print(f"Logged in and the current url is : {driver.current_url}")
            return True
    except TimeoutException:
        print("Desired url was not rended within the time limit")
        return False


def navigate_to_jobs_page():
    if validate_home():
        try:
            driver.get(linkedin_jobs)
            validate_jobs_page = WebDriverWait(driver, 10).until(
                EC.url_to_be((linkedin_jobs))
            )
            if validate_jobs_page:
                print(f"Were here at the jobs page! Good Work. {driver.current_url}")
        except TimeoutException:
            print("Desired url was not rended within the time limit")

def get_next_button_id():

    
    page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, "html.parser")
    
    next_button = soup.find_all(attrs={"aria-label" : "View next page" })

    attribute = None
    
    for id in next_button:
        attribute = id.get('id')
        
    if attribute:
    
        print(f'NEXT BUTTON ID: {attribute}')
        return attribute    
    else:
        print("No ID Found")
        return None    
    
def get_job_count():
    pass

def validate_jobs_page():
    try:
        validate_jobs_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#main div div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow div.scaffold-layout__list div ul",
                )  # Checks for list container to be located/loaded.
            )
        )
        if validate_jobs_page:
            print(f"Logged in and the current url is : {driver.current_url}")
            return True
    except TimeoutException:
        print("Desired url was not rended within the time limit")
        return False


def scroll_in_container(container):
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)

    while True:

        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", container
        )
        time.sleep(3)

        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", container
        )
        if new_height == last_height:
            break
        last_height = new_height


def get_jobs_links():
    if validate_jobs_page():
        counter = 0
        job_storage = {}
    try:
        while True:

            container = driver.find_element(
                By.CSS_SELECTOR, "div.jobs-search-results-list"
            )
            scroll_in_container(container)

            jobs = driver.find_elements(By.CSS_SELECTOR, "a.job-card-list__title")

            for job in jobs:
                counter += 1
                job_title_element = job.text
                job_link = job.get_attribute("href")
                print(colored(f"Job Title: {job_title_element}", "green"))
                print(colored(f"Job Link: {job_link}", "blue"))
                print(colored(counter, "red"))

                job_storage[job_title_element] = job_link
            
            next_button_id = get_next_button_id()
            if next_button_id:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, next_button_id))
                )
                
                next_button.click()
            else:
                WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
                print("No more pages to load")
                break
                    
           

    except Exception as error:
        print(f"Error while getting links: {error}")
        raise error

    pprint(f"Jobs Links Dict: {job_storage}")

    return job_storage


init_sign_in()
navigate_to_jobs_page()
get_jobs_links()

# driver.quit()
