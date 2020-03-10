import requests
from . import ConsumerApiWrapper, Exception404, Exception409


class UserNotFoundException(Exception404):
    def __init__(self):
        super().__init__(message="User not found.")


class UserAlreadyExistsException(Exception409):
    def __init__(self):
        super().__init__(message="User already exists.")


class UserWrapper(ConsumerApiWrapper):
    """Wraps users and me endpoints of the Consumer API. Consumers can retrieve more information about themselves (me)
    than they can about other users."""

    @staticmethod
    def process_status(status_code: int, desc: str = None) -> None:
        """Raise class-specific exceptions corresponding to API errors."""
        if status_code == 404:
            raise UserNotFoundException
        elif status_code == 409:
            raise UserAlreadyExistsException
        else:
            super().process_status(status_code, desc)

    def post(self) -> dict:
        """Create new user from an access token.

        The sub claim in the decoded token uniquely identifies a user.

        Makes a POST request to the :ref:`Users <UsersConsumerAPI>` endpoint.

        Returns:
            Dictionary representing a user.

        """
        usersurl = "{apiurl}/users".format(apiurl=self.apiurl)
        try:
            r = requests.post(usersurl, headers=self.headers)
            response = r.json()
        except requests.exceptions.RequestException as e:
            UserWrapper.process_status(e.response.status_code, str(e))
        return response

    def delete(self) -> None:
        """Delete current user.

        Consumer API permits users to delete their own database entry.

        Makes a DELETE request to the :ref:`Me <MeConsumerAPI>` endpoint.

        Current user is identified by an access token passed to the :py:func:`constructor <ConsumerApiWrapper.__init__>`.

        Returns:
            None

        """
        meurl = "{apiurl}/me".format(apiurl=self.apiurl)
        try:
            requests.delete(meurl, headers=self.headers)
        except requests.exceptions.RequestException as e:
            UserWrapper.process_status(e.response.status_code, str(e))

    def get(self) -> dict:
        """Get current user.

        Retrieves database record for the current user.

        Makes a GET request to the :ref:`Me <MeConsumerAPI>` endpoint.

        Current user is identified by an access token passed to the :py:func:`constructor <ConsumerApiWrapper.__init__>`.

        Returns:
            dict: API representation of the current user.

        """
        meurl = "{apiurl}/me".format(apiurl=self.apiurl)
        try:
            r = requests.get(meurl, headers=self.headers)
            response = r.json()
        except requests.exceptions.RequestException as e:
            UserWrapper.process_status(e.response.status_code, str(e))
        return response
