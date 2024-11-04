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
import geocoder

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument(f"--user-data-dir={profile_dir}")


driver = webdriver.Chrome(options=chrome_options)

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TEST_JOB_URL = "https://www.linkedin.com/jobs/view/4057290270/?eBP=CwEAAAGS-VXq_1498WQR2FCU6AXR3XU3gFDoZA9OkfV4TOlmkVz8jKLK5KJcpXd8N35CKQqJgBFvJIuMUaQyL0A8e0FICq8iaLmFFnS-Rv8ldQYGoX170CvhHBnn9RQVIY6x2jwY-LWsxq6dzrTmzdJjdXa4wlLtXzB7FneY9BfvefepvidsJwLdXkbBGw4BbUggAD0xlQKT7-zUYqMCo4aL8-W7BCBsKltkYCUpLuN1-nMy7qoCXFxboiFVvMgnxyvjaMhseNNu9xLzoRT6YtwBrDsvVvjxq9O0NidDOIgYAeeOaIo8qms3qzFdwc3RWN02Z3CQwLn0_tKJaw_nTTk5hQxY7vqm-tiMyfY5tP84pU3CSMjsYC1VUi1VZiVJr1UD_kYOn1fe-1cJGxTtoN1ABXSTmQ1u7iqqMiPibsxtG_AOunG-xLX2Fz0Nn70OM8QPeyYDPlrXu3pt-rZXAUJ3CnvHuycfBOtnIE0_FmTnCTkHLe8hmzkhIP11H-A&refId=X3dgMSycwzvbedIhEl1%2BNQ%3D%3D&trackingId=2dQk2vcXJO7zFArHAw%2BueQ%3D%3D&trk=flagship3_search_srp_jobs&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_jobs%3B1YASEOGqS1KIrTGWMF1yHQ%3D%3D&lici=2dQk2vcXJO7zFArHAw%2BueQ%3D%3D"

LINKEDIN_HOME = "https://www.linkedin.com/home"
LINKEDIN_JOBS = "https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&geoId=104116203&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER"


def init_sign_in():
    driver.get(LINKEDIN_HOME)

    try:
        sign_in_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
        )
        driver.execute_script("arguments[0].click()", sign_in_link)

        if EMAIL is None or PASSWORD is None:
            raise ValueError("EMAIL or PASSWORD is not set, check your .env file, foo.")

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
        raise NoSuchElementException(f"Cant find element. Details: {str(error)}")
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
            driver.get(LINKEDIN_JOBS)
            validate_jobs_page = WebDriverWait(driver, 10).until(
                EC.url_to_be((LINKEDIN_JOBS))
            )
            if validate_jobs_page:
                print(f"Were here at the jobs page! Good Work. {driver.current_url}")
        except TimeoutException:
            print("Desired url was not rended within the time limit")


def get_button_id(attribute_args):

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    button = soup.find_all(attrs=attribute_args)

    attribute = None

    for id in button:
        attribute = id.get("id")

    if attribute:

        print(f"BUTTON ID: {attribute}")
        return attribute
    else:
        print(f"No ID Found\n At URL:{driver.current_url}")

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
                )
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
        job_storage = []
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
                job_storage.append(job_link)
                # job_storage[job_title_element] = job_link

            next_button_id = get_button_id({"aria-label": "View next page"})
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

    # pprint(f"Jobs Links Dict: {job_storage}")

    return job_storage


def open_new_tab(job_url):
    driver.execute_script(f"window.open('{job_url}', '_blank');")
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[-1])
    print(f"swtiched to a new window at {driver.current_url}")


def close_tab():
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def apply_to_jobs(job_url):
    open_new_tab(job_url)

    quick_apply_button_id = get_button_id({"aria-label": re.compile("Easy Apply to")})

    if driver.current_url:
        print("current page is valid")

        quick_apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, quick_apply_button_id))
        )
        quick_apply_button.click()
        print(
            f"Pretending to click on {quick_apply_button} Button with the id of: {quick_apply_button_id}"
        )

    else:
        print("not so valid")


init_sign_in()
navigate_to_jobs_page()
get_jobs_links()

# driver.quit()

# open_new_tab(test_job_url)

apply_to_jobs(TEST_JOB_URL)
