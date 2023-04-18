# CTJ: Level Up Your Career - A Canadian Job Site for Tech Professionals with an XP Bar

Welcome to our project for Hack The Break 2023! We've created a job site specifically tailored for tech professionals seeking opportunities in Canada. Our platform not only showcases relevant job postings but also features an XP bar to help track your progress and maintain motivation during the job search.

Our tech stack includes Python, SQL, HTML, CSS, and JavaScript.

*Team members: Anton, Duncan, Leo, Nick.*

## Scraper

Our job postings are scraped from LinkedIn using the [LinkedIn API](https://github.com/tomquirk/linkedin-api), Beautiful Soup 4, and Selenium WebDriver.

**To run the scraper:**

1. Install the required dependencies:
   
`pip3 install -r requirements.txt`

2. Change to the `scraping` directory:

`cd scraping`

3. Create a `.env` file with your LinkedIn email and password, using the following variable names:

`EMAIL=your_email@example.com`
`PASSWORD=your_password`

4. Run the main script:

`python3 main.py`


The relevant job postings will be saved to the `jobs.json` file. Please note that the scraper may take some time to execute due to the built-in delay designed to avoid CAPTCHAs.

## TCP Server

*To be provided by Duncan.*

## SQL Server

*To be provided by Leo.*

## Future Plans

- Improve the scraper to fetch job postings from other websites
- Add a filter for remote job opportunities
- Expand our database to cover all fields and allow employers to post jobs directly on our platform
- Enhance the frontend and transition to the MERN stack for a more robust solution
