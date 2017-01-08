import json

import requests
from weibo import APIClient

APP_KEY = '1994694879'
APP_SECRET = 'aaece73e09aa2ccc0b622f82ad021fef'
#req_api = 'https://api.weibo.com/2/statuses/timeline_batch.json'
req_api = 'https://api.weibo.com/2/statuses/user_timeline.json'
authorize_url = 'https://api.weibo.com/oauth2/authorize'
get_authorized_token_url = 'https://api.weibo.com/oauth2/access_token'
callback_url = 'http://127.0.0.1'


def _authorize():
    rr = requests.post(authorize_url,
                       data={
                           'client_id': APP_KEY,
                           'redirect_uri': callback_url
                       })
    print rr.status_code, rr.content


def _get_authorized_token(code):
    print('get authorized token with code {}'.format(code))
    rrr = requests.post(get_authorized_token_url,
                        data={
                            'client_id': APP_KEY,
                            'client_secret': APP_SECRET,
                            'grant_type': 'authorization_code',
                            'code': code,
                            'redirect_uri': callback_url
                        })
    return rrr.json()['access_token']


def _extract_code(url):
    print(url)
    return '58b6f6fc99f7d4af9486f06787d039aa'


def _get_access_token():
    client = APIClient(APP_KEY, APP_SECRET, callback_url)
    _url = client.get_authorize_url()
    code = _extract_code(_url)
    res = client.request_access_token(code)
    client.set_access_token(res.access_token, res.expires_in)
    return res['access_token']

# 'uids': [1727721727]
if __name__ == '__main__':
    # access_token = _get_access_token()
    # access_token = _get_authorized_token('58b6f6fc99f7d4af9486f06787d039aa')
    _authorize()
    print('------')
    access_token = '2.00K5JYJBDQXzKCcb33f520417RifIB'
    print('request with token: {}'.format(access_token))
    r = requests.get(req_api,
                     params=json.dumps({
                         'access_token': access_token
                     }),
                     headers={'Content-Type': 'application/json'})
    print('status_code: {}'.format(r.status_code))
    print(r.json())
