from enum import IntEnum
import requests
from typing import Optional
from .search_result import Search, Page
from pprint import pformat
import logging

__name__ = 'companieshouse'
__version__ = '0.1'


BASE_URI = 'https://api.companieshouse.gov.uk'

# API routes
class Routes():
    """Internal usage only

    """

    class MetaSearch(type):
        class InvalidSearchType(Exception):
            pass

        All = BASE_URI + '/search'
        Company = BASE_URI + '/search/companies'
        Officer = BASE_URI + '/search/officers'

        @classmethod
        def __getitem__(cls, index):
            if isinstance(index, int) and 1 <= index <= 3:
                return (cls.Company, cls.Officer, cls.All)[index - 1]

            else:
                raise InvalidSearchType

    class Search(object, metaclass=MetaSearch):
        pass

    class Company():
        Get = BASE_URI + '/company'


class InternalServerError(Exception):
    """Exception raised when a 500 error is received

    """
    pass

class InvalidAuthToken(Exception):
    """Exception raised when the authentication is invalid

    """
    pass

class InvalidIPOrDomain(Exception):
    """Exception raised due to some other validation failing (403 with no body)

    """
    pass

class BadRequest(Exception):
    """Exception raised due to bad request (400)

    """
    pass

# IntEnum such that it can be combined through binary OR
class SearchType(IntEnum):
    """Used for specifying the types of entities you wish to query

    """
    Company = 0b01
    Officer = 0b10
    All = 0b11


# Class to be created for usage in querying API
class Querier():
    """Represents a querier used for retrieving data from the API and making objects

    """

    def __init__(self, auth_token: str):
        self._auth_token = auth_token

    # Deal with an issue with a request
    @staticmethod
    def _handle_error(request):
        logging.debug('Error occured: HTTP {}'.format(request.status_code))

        if request.status_code == 401:
            raise BadRequest

        elif request.status_code == 403:
            if request.text == '':
                raise InvalidIPOrDomain('Either your IP address does not match the IP on your application or you haven\'t added `https://local.sender` as a JavaScript domain')

            else:
                raise InvalidAuthToken

        elif request.status_code == 500:
            raise InternalServerError

        elif request.status_code == 416:
            return None

    def _create_request(self, route, callback):
        """Internal use only: create and send a request and pass the data either to the error handler or into a callback function

        """

        request = requests.get(route, auth=(self._auth_token, ''), headers={'Origin': 'https://local.sender'})

        if request.status_code != 200:
            self._handle_error(request)

        else:
            data = request.json()

            logging.debug('Received the following data: {}'.format(pformat(data)))

            return callback(data)

    # Function performs search query returning new searchresults with one page
    def create_search(self, query: str, search_type: int=SearchType.All) -> Optional[Search]:
        """Create a new Search object

        """
        return Search(query, search_type, self)

    # Function turns search query into request, sends request, converts request into search result
    def get_search_page(self, query: str, search_type: int=SearchType.All, page_size: int=15, start_at: int=0) -> Optional[Page]:
        """Internal use only: used to get a Page object

        """

        def _handle_results(data) -> (Page, int):
            search_results = data['items']

            p = Page(self, search_results)

            return p, data['total_results']


        return self._create_request(

            '{}?q={}&start_index={}&items_per_page={}'.format(
                    Routes.Search[search_type],
                    query,
                    start_at,
                    page_size,
                    ),

            _handle_results
            )

    # Get more details regarding a company
    def get_company(self, company_id):
        """Internal use only: used to get a company object

        """

        def _handle_results(data) -> None:
            print(data)

        return self._create_request(

            '{}/{}'.format(
                Routes.Company.Get,
                company_id,
                ),

            _handle_results
            )
