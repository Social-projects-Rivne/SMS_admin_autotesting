import requests
import sys
import os
sys.path.insert(0,
                os.path.dirname(os.path.dirname
                                (os.path.abspath(__file__))))
from config import credentials, USERNAME, PASSWORD


class RequestGenerator:

    """This class contains methods to generate requests
    to check whether the controller functionality works correctly"""

    def __init__(self, port=''):
        self.user = USERNAME
        self.password = PASSWORD
        self.host = credentials[0] + [':' + str(port), ''][port == '']
        self.url_host = 'http://' + credentials[0]\
                        + [':' + str(port), ''][port == '']
        self.session = ''

        # define urls for requests
        self.url_home = self.url_host
        self.url_index = self.url_home + '/index'
        self.url_users_list = self.url_home + '/users_list'
        self.url_user_add = self.url_home + '/user_add'
        self.url_user_remove = self.url_home + '/user_remove/'
        self.url_user_update = self.url_home + '/user_update/'
        self.url_schools_list = self.url_home + '/schools_list'
        self.url_school_add = self.url_home + '/school_add'
        self.url_school_remove = self.url_home + '/school_remove'
        self.url_school_update = self.url_home + '/school_update'
        self.url_subjects_list = self.url_home + '/subjects_list'
        self.url_subject_add = self.url_home + '/subject_add'
        self.url_subject_remove = self.url_home + '/subject_remove'
        self.url_subject_update = self.url_home + '/subject_update'
        self.url_login = self.url_home + '/login'
        self.url_logout = self.url_home + '/logout'

        # common headers
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'uk-UA,uk;q=0.8,ru;q=0.6,en-US;q=0.4,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': self.host,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.110 Safari/537.36'
        }
        # common data
        self.data = dict()

    def _send_request(self, url, as_logged_in=True, method='GET',
                      headers=False, data=False, allow_redirects=True):

        if as_logged_in:

            if self.session == '':
                creds = {
                    'username': self.user,
                    'password': self.password
                }
                resp = requests.post(self.url_login,
                                     headers=self.headers, data=creds)
                if resp.status_code == 200:
                    if 'session' in resp.cookies:
                        self.session = resp.cookies['session']

            headers['Cookie'] = 'session=' + self.session + ';'

        response = ''
        if method == 'GET':

            if headers and not data:
                response = requests.get(url,
                                        headers=headers,
                                        allow_redirects=allow_redirects)
            elif headers and data:
                response = requests.get(url,
                                        headers=headers,
                                        params=data,
                                        allow_redirects=allow_redirects)
            elif not headers and not data:
                response = requests.get(url,
                                        allow_redirects=allow_redirects)
            elif not headers and data:
                response = requests.get(url,
                                        params=data,
                                        allow_redirects=allow_redirects)

        elif method == 'POST':

            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Cache-Control'] = 'max-age=0'
            headers['Origin'] = self.url_home

            if headers and not data:
                response = requests.post(url,
                                         headers=headers,
                                         allow_redirects=allow_redirects)
            elif headers and data:
                response = requests.post(url,
                                         headers=headers,
                                         allow_redirects=allow_redirects,
                                         data=data)
            elif not headers and not data:
                response = requests.post(url,
                                         allow_redirects=allow_redirects)
            elif not headers and data:
                response = requests.post(url,
                                         allow_redirects=allow_redirects,
                                         data=data)

        # automatically refresh cookie.session value
        if response.status_code == 200:
            if 'session' in response.cookies:
                self.session = response.cookies['session']

        return response

    # --------------------------------------------------
    # login/logout
    # --------------------------------------------------
    def login(self, user=USERNAME, password=PASSWORD, as_logged_in=True):
        self.data = {
            'username': user,
            'password': password
        }
        response = self._send_request(self.url_login, as_logged_in,
                                      'POST', self.headers, self.data)
        return response

    def logout(self):
        response = self._send_request(self.url_logout, headers=self.headers,
                                      allow_redirects=False)
        return response

    # --------------------------------------------------
    # teacher CRUD
    # --------------------------------------------------
    def get_users_list(self, as_logged_in='true', method='GET'):
        allow_redirects = as_logged_in
        response = self._send_request(self.url_users_list,
                                      as_logged_in=as_logged_in,
                                      method=method, headers=self.headers,
                                      allow_redirects=allow_redirects)
        return response

    def add_user(self, data, as_logged_in='true', method='POST'):
        allow_redirects = False
        self.headers['Referer'] = self.url_user_add
        response = self._send_request(self.url_user_add,
                                      as_logged_in=as_logged_in,
                                      method=method, headers=self.headers,
                                      data=data,
                                      allow_redirects=allow_redirects)
        return response

    def update_user(self, user, method='POST', as_logged_in=True):
        response = self._send_request(url=self.url_user_update +
                                      str(user['id']),
                                      headers=self.headers, data=user,
                                      allow_redirects=False, method=method,
                                      as_logged_in=as_logged_in)
        return response

    def delete_user(self, user, method='POST', as_logged_in=True):
        self.headers['Referer'] = self.url_user_remove + str(user['id'])
        self.data = {
            'delete_button': '%D0%A2%D0%B0%D0%BA'
        }
        response = self._send_request(url=self.url_user_remove +
                                          str(user['id']),
                                      headers=self.headers, data=self.data,
                                      allow_redirects=False, method=method,
                                      as_logged_in=as_logged_in)
        return response
