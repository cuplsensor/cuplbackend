import requests
from . import ConsumerApiWrapper, Exception404, Exception409


class UserNotFoundException(Exception404):
    def __init__(self):
        super().__init__(message="User not found.")


class UserAlreadyExistsException(Exception409):
    def __init__(self):
        super().__init__(message="User already exists.")


class UserWrapper(ConsumerApiWrapper):
    @staticmethod
    def process_status(status_code, desc=None):
        """ Raise an exception for HTTP error statuses"""
        if status_code == 404:
            raise UserNotFoundException
        elif status_code == 409:
            raise UserAlreadyExistsException
        else:
            ConsumerApiWrapper.process_status(status_code, desc)

    def post(self):
        usersurl = "{apiurl}/users".format(apiurl=self.apiurl)
        r = requests.post(usersurl, headers=self.headers)
        response = r.json()
        UserWrapper.process_status(r.status_code)
        return response

    def delete(self):
        meurl = "{apiurl}/me".format(apiurl=self.apiurl)
        r = requests.delete(meurl, headers=self.headers)
        UserWrapper.process_status(r.status_code)

    def get(self):
        meurl = "{apiurl}/me".format(apiurl=self.apiurl)
        try:
            r = requests.get(meurl, headers=self.headers)
        except requests.exceptions.RequestException as e:
            UserWrapper.process_status(e.response.status_code, e.data)
        response = r.json()
        return response

    def __init__(self, baseurl, tokenstr):
        super().__init__(baseurl, tokenstr)