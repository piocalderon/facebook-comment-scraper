import requests
import time
import pandas as pd
import random

token = '' #FB Graph API access token

def return_request_url(site):
    return '{}?fields=posts.limit(10){comments{message,created_time,comments.limit(5)},message,created_time}'.format(site)

    if type(row) != float:
        for com in row['data']:
            if 'from' in com.keys():
                if com['from']['name'] == owner:
                    return com['message']
    else:
        return ''

lim_count = 0

# for example, home credit
site = 'homecreditph'
owner = 'Home Credit'

post_resp = requests.get('https://graph.facebook.com/v2.11/' + return_request_url(site), {'access_token': token})    

# running will be a df with post message, comment, and first-level owner reply for each comment and post on the fb page 
running = pd.DataFrame()

while True:
    if lim_count == 0:
        rjson = post_resp.json()['posts']
    else:
        rjson = post_resp.json()
    for i in range(len(rjson['data'])): # loop over posts
        print('Looking at post {}...'.format(10*lim_count+i))
        if 'message' in rjson['data'][i].keys():
            print('   Body {}: {}'.format(i, rjson['data'][i]['message'][:70]))
        first = True
        try: # put comments in a df
            comments_for_post = pd.DataFrame(rjson['data'][i]['comments']['data'])
        except:
            comments_for_post = pd.DataFrame()
        while True:
            if first == True:
                try:
                    # go to next page of comments
                    comments_url = rjson['data'][i]['comments']['paging']['next']
                except:
                    break
            # put a buffer to go over rate limit
            time.sleep(random.randint(2,5))
            r = requests.get(comments_url)
            comments_data = r.json()['data']
            comments_for_post = pd.concat([comments_for_post, pd.DataFrame(comments_data)], ignore_index=True)
            try:
                # go to next page of comments
                comments_url = r.json()['paging']['next']
                first = False
            except KeyError:
                break
        print('   Number of comments: {}'.format(comments_for_post.shape[0]))
        if 'comments' in comments_for_post.columns:
            comments_for_post['reply'] = comments_for_post['comments'].map(lambda x: process_dict(x, owner))
            comments_for_post = comments_for_post.drop(['comments'], axis=1)
        if 'id' in comments_for_post.columns:
            comments_for_post = comments_for_post.drop(['id'], axis=1)
        if 'message' in rjson['data'][i].keys():
            comments_for_post['post'] = rjson['data'][i]['message']
        else:
            comments_for_post['post'] = ''
        running = pd.concat([running, comments_for_post], ignore_index=True)
    post_url = rjson['paging']['next']
    post_resp = requests.get(post_url)
#         if lim_count == 9: # if this is not set, loop over all posts in the page
#             break
    lim_count += 1

