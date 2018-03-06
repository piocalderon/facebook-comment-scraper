Facebook Scraper - scrape comments and reviews from Facebook public pages

comment_scraper.py : uses Facebook Graph API to extract comments (and first-level reply of site admin) from a public FB page
review_scraper.py: uses Selenium and Beautiful Soup to extract reviews from a public FB page (Facebook Graph API requires a page-admin-level token to access reviews so we have to do it manually here)