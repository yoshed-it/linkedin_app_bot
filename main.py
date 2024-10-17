from selenium import webdriver
import db
import scraper

# driver = webdriver.Chrome()

database = db.create_table()

# scraper.init_sign_in()
# scraper.navigate_to_jobs_page()

# job_links = scraper.get_jobs_links()

# for job in job_links:
#     database = db.insert_job(job)
full_job_list = db.get_job_list()

for job in full_job_list:
    print(job)


# scraper.get_jobs_links()