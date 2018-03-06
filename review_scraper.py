from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def initialize_page(name):
    browser.get('https://www.facebook.com/pg/{}/reviews/?ref=page_internal'.format(name))
    stars = browser.find_elements_by_class_name('_3uzu')[:5]
    stars[0].click()
    return browser

def exhaust_posts(browser):
	while True:
	    more = browser.find_elements_by_css_selector('a.pam.uiBoxWhite.noborder.uiMorePagerPrimary')
	    for i in more:
	        try:
	            i.click()
	            break
	        except:
	            pass
	    if len(more) == 2:
	        break

def collect_reviews(browser):
    posts = browser.find_elements_by_css_selector('div._1dwg._1w_m._q7o')
    return posts

def extract_review(post):
    bs = BeautifulSoup(post.get_attribute('innerHTML'), 'lxml')
    rating = int(bs.select('i')[0].text[0])
    text = ' '.join([p.text for p in bs.select('p')])
    return text, rating

def save_csv_of_reviews(browser, name):
	posts = collect_reviews(browser)
	reviews = []
	for index, post in enumerate(posts):
	    try:
	        print(index, extract_review(post)[0][:40])
	        reviews.append(extract_review(post))
	    except:
	        continue
	reviews = pd.DataFrame(reviews, columns=['text', 'rating'])
	reviews.to_csv('reviews_{}.csv'.format(name), index=False)

def main(name):
	browser = initialize_page(name)
	save_csv_of_reviews(browser, name)

if __name__ == '__main__':
	# name is the identifier of the page in the URL
	name = input('Enter name of FB page with review tab: ')
	main(name)
