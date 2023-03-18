# CTJ : Level Up Your Career - A Canadian Job Site for Tech Professionals with an XP Bar

Our project for Hack The Break 2023. We have created a job site, targetted for those working in Canada based tech jobs. We started by scraping job postings for LinkedIn, using https://github.com/tomquirk/linkedin-api, which uses the Voyager endpoints to find job postings and their relevent fields. 

We set up an SQL server to store all our data and a TCP server program to handle all the http requests to the server. We realize that applying for jobs can be tiring, and took inspiration from Dulingo, and added an XP bar, to signify progress. 

We used Python, SQL, HTML, CSS & JS for this project. 

Cheers,

Anton, Duncan, Leo, Nick.

## Scraper

The scraper was built with Python, using the LinkedIn API, beautifulsoup4, Selenium webdriver. 

To run the scraper, do the following:
<br/>
`pip3 install requirements.txt`
<br/>
`cd scraping`
<br/>
Place your linkedIn account password, and email in a .env, with the names "PASSWORD" and "EMAIL"
<br/>
`python3 main.py`
<br/>

Relevent job postings will be put into the `jobs.json` file. Note that this may take a while, as the LinkedIn scraper has a delay, to avoid CHALLENGES.

## TCP server

Duncan to comment. 

## SQL server

Leo to comment.

## Future plans? 

We plan to improve the scraper, to get job postings from other sites, and add the option to filter on the website for only remote jobs. We also hope to expand our database, in order to offer postings on all fields, and allow employers to post jobs within our site. 

We also plan to improve our frontend, and learn the MERN stack in the process. 