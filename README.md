# linkedin_app_bot
LinkedIn easy apply bot

Unfortunatly do to an oopsie on my part, AKA, I didnt do my research, AKA when trying to use the quick apply button, after hitting next a few times, 
linked in now requires you to answer some questions about your experience. Until I can figure out how to handle that whole bag of worms... I'm thinking this script, while cool as hell in theory, might be down for the count. 

That being said....

If you would like to play around with it, its pretty simple.

install required dependancies

create a .env file following this convention
EMAIL="linked_in_email"
PASSWORD="linked_in_password"

Youll also need to update the TEST_JOB_URL with a valid linkedin job url.

If you want to scrape all the jobs based on the current job search, which is "Python Developer, Seattle, Distance 25" GREAT! otherwise youll need to find your own geocode from the search bar. This was on my todo list, but... since the project is now defunkt... ill probably wait on this feature.

To do the scrapy scrapy just run the script and watch the magic happen (now in color!)

What should happen:
Youll get logged into linkedin
The script will grab every job based on your search criteria
when thats all done a new tab will open and start the whole application process for the test job. 

The idea was, to take all of the job links, add them to a lil light weight database. The apply to job would collect the links from the DB and "methodically" apply to each job. 

The proof of concept works. 

In the future, I think the scraper is still useful to maybe, pass the job details to h20gpt and filter out what jobs are spam, which jobs (based on your resume) you qualify for, with link provided. 

It could be a useful little tool. 


