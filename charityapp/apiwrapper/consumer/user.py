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
    def process_status(status_code):
        """ Raise an exception for HTTP error statuses"""
        if status_code == 404:
            raise UserNotFoundException
        elif status_code == 409:
            raise UserAlreadyExistsException
        else:
            ConsumerApiWrapper.process_status(status_code)

    def post(self):
        usersurl = "{consumerapiurl}/users".format(consumerapiurl=self.consumerapiurl)
        r = requests.post(usersurl, headers=self.headers)
        response = r.json()
        UserWrapper.process_status(r.status_code)
        return response

    def delete(self):
        meurl = "{consumerapiurl}/me".format(consumerapiurl=self.consumerapiurl)
        r = requests.delete(meurl, headers=self.headers)
        UserWrapper.process_status(r.status_code)

    def get(self):
        meurl = "{consumerapiurl}/me".format(consumerapiurl=self.consumerapiurl)
        r = requests.get(meurl, headers=self.headers)
        UserWrapper.process_status(r.status_code)
        response = r.json()
        return response

    def __init__(self, tokenstr):
        super().__init__(tokenstr)