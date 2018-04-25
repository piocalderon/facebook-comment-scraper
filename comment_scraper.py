import requests
import time
import pandas as pd
import random

running = pd.DataFrame()

site = 'homecreditph'
owner = 'Home Credit'

token = 'EAACmU0a4eqoBANu3ba3JUpFFi6r1FeKZCD1HfR5s9Wy9VETJ7k3ScUXZB9imgRhczzIJVh3m20OmjaNPxaTLPZAyH0AkR6iZB3QQO6zFDTYx0I1I0OjumpLMiBxlOFjdn8gRhlJ9eoeo5xUFbTj2nzTkLxppE5cZD' #FB Graph API access token
req = site + '?fields=posts.limit(10){comments{message,created_time,comments.limit(5)},message,created_time}'

def process_dict(row):
    if type(row) != float:
        for com in row['data']:
            if 'from' in com.keys():
                if com['from']['name'] == 'GCash':
                    return com['message']
    else:
        return ''

lim_count = 0

post_resp = requests.get('https://graph.facebook.com/v2.11/' + req, {'access_token': token})    
while True:
#     print("lim", lim_count)
    if lim_count == 0:
        rjson = post_resp.json()['posts']
    else:
        rjson = post_resp.json()
    for i in range(len(rjson['data'])):
        print('Looking at post {}...'.format(10*lim_count+i))
        if 'message' in rjson['data'][i].keys():
            print('   Body {}: {}'.format(i, rjson['data'][i]['message'][:70]))
        first = True
        try:
            comments_for_post = pd.DataFrame(rjson['data'][i]['comments']['data'])
        except:
            comments_for_post = pd.DataFrame()
        while True:
            if first == True:
                try:
                    comments_url = rjson['data'][i]['comments']['paging']['next']
                except:
                    break
#                     print(comments_url)
            time.sleep(random.randint(2,5))
            r = requests.get(comments_url)
            comments_data = r.json()['data']
#                 print('before', comments_for_post.shape)
            comments_for_post = pd.concat([comments_for_post, pd.DataFrame(comments_data)], ignore_index=True)
#                 print('after', comments_for_post.shape)
            try:
                comments_url = r.json()['paging']['next']
#                     print(comments_url)
                first = False
            except KeyError:
                break
        print('   Number of comments: {}'.format(comments_for_post.shape[0]))
        if 'comments' in comments_for_post.columns:
            comments_for_post['reply'] = comments_for_post['comments'].map(process_dict)
            comments_for_post = comments_for_post.drop(['comments'], axis=1)
        if 'id' in comments_for_post.columns:
            comments_for_post = comments_for_post.drop(['id'], axis=1)
        if 'message' in rjson['data'][i].keys():
            comments_for_post['post'] = rjson['data'][i]['message']
        else:
            comments_for_post['post'] = ''
        running = pd.concat([running, comments_for_post], ignore_index=True)
    post_url = rjson['paging']['next']
#         print('POST', post_url)
    post_resp = requests.get(post_url)
#         if lim_count == 9: # if this is not set, loop over all posts forever
#             break
    lim_count += 1

running.to_csv('{}.csv'.format(site))



# # to go to lim_count
# lim_count = 0
# post_resp = requests.get('https://graph.facebook.com/v2.11/' + req, {'access_token': token})  
# while lim_count != 47:
#     print(lim_count)
#     post_url = rjson['paging']['next']
#     if lim_count == 0:
#         rjson = post_resp.json()['posts']
#     else:
#         rjson = post_resp.json()
#     post_url = rjson['paging']['next']
#     post_resp = requests.get(post_url)
#     lim_count += 1

