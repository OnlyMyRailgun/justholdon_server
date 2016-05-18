import requests

class Weiboer(object):
    # get token info
    def get_info(self, access_token):
        r = requests.post('https://api.weibo.com/oauth2/get_token_info', data={'access_token':access_token})
        return r.json()
    
    # get user detail info
    def get_detail_info(self, access_token, uid=None):
        if uid is None:
            r = self.get_info(access_token)
            uid = r[u'uid']
        r = requests.get('https://api.weibo.com/2/users/show.json', params={'access_token':access_token, 'uid':uid})
        return r.json()