# LinkedIn Easy Apply Bot 🚀

Welcome to the **LinkedIn Easy Apply Bot**—an automated way to save time applying for jobs on LinkedIn! This bot logs into your LinkedIn account, scrapes job listings based on your search criteria, and (in theory) goes through the “Easy Apply” process. 
Unfortunatly do to an oopsie on my part, AKA, I didnt do my research, AKA when trying to use the quick apply button, after hitting next a few times, 
linked in now requires you to answer some questions about your experience. Until I can figure out how to handle that whole bag of worms... I'm thinking this script, while cool as hell in theory, might be down for the count. 

That being said....

### Quick Start Guide

1. **Install Dependencies**

   First, install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. **Set Up Your Environment**

   Create a .env file to securely store your LinkedIn login details. Your .env file should follow this format:

     ```bash
     EMAIL="your_linked_in_email"
     PASSWORD="your_linked_in_password"
     ```

3. **Update the Test Job URL**
 
   Set the ```TEST_JOB_URL``` variable in the script to a valid LinkedIn job URL. This job will be used as the test case for the application process.
   (Optional) Set Custom Search Criteria
   The bot currently defaults to the following search parameters:
   
     ```bash
     Job Title: Python Developer
     Location: Seattle
     Distance: 25 miles
     ```

   If you’d like to use different search criteria, feel free to adjust them in the script. You’ll also need to find your specific LinkedIn geocode for the desired location (available from the LinkedIn job search URL).
   Run the Bot
   Once everything’s set, run the script to start the bot:
     
     ```bash
     python linkedin_app_bot.py
     ```

   Sit back, grab a beer, and watch as the bot:
   
   - Logs into LinkedIn.
   - Scrapes all job links based on your search criteria.
   - Opens a new tab to begin the “Easy Apply” process on the test job.

4. **What Actually Happens**
 
   Scraping: All job links matching your search criteria are scraped and saved.
   Applying: The bot opens a new tab and begins applying to the test job you specified. Although the auto-apply feature is paused due to LinkedIn's new questions, this portion still serves as a proof of concept.


5. **Future Enhancements**

   In the future, this bot could do more than just auto-apply. Ideas include:
   
   Passing job details to an AI model (like H2O GPT) to filter out spam or low-quality jobs.
   Matching jobs to your resume to identify roles you’re highly qualified for.
   Providing a direct link to jobs worth applying to.
   If you want to customize this script or take it for a spin, have at it! It’s a work in progress but could become a handy tool for job hunting and lead generation.
   
   Happy job hunting! 🕵️‍♂️✨
