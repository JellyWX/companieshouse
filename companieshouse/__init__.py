from enum import IntEnum
import requests
from typing import Optional
from .search_result import Search, Page, OfficerListPage
from pprint import pformat
import logging

__name__ = 'companieshouse'
__version__ = '0.1'


BASE_URI = 'https://api.companieshouse.gov.uk'

# API routes
class Routes():
    """Internal usage only

    """

    Search = BASE_URI + '/search/companies'

    class Company():

        @staticmethod
        def Get(c):
            return BASE_URI + '/company/{}'.format(c)

        @staticmethod
        def Officers(c):
            return BASE_URI + '/company/{}/officers'.format(c)


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
    def create_search(self, query: str) -> Optional[Search]:
        """Create a new Search object

        """
        return Search(query, self)

    # Function turns search query into request, sends request, converts request into search result
    def get_search_page(self, query: str, page_size: int=15, start_at: int=0) -> Optional[Page]:
        """Internal use only: used to get a Page object

        """

        def _handle_results(data) -> (Page, int):
            search_results = data['items']

            p = Page(self, search_results)

            return p, data['total_results']


        return self._create_request(

            '{}?q={}&start_index={}&items_per_page={}'.format(
                    Routes.Search,
                    query,
                    start_at,
                    page_size,
                    ),

            _handle_results

            )

    def get_officer_list_page(self, company_id: str, page_size: int=15, start_at: int=0) -> Optional[Page]:

        def _handle_resp(data) -> (Page, int):

            search_results = data['items']

            p = OfficerListPage(self, search_results)

            return p, data['total_results']

        return self._create_request(

            '{}?start_index={}&items_per_page={}'.format(
                    Routes.Company.Officers(company_id),
                    start_at,
                    page_size,
                    ),

            _handle_resp

            )

    # Get more details regarding a company
    def get_company(self, company_id):
        """Internal use only: used to get a company object

        """

        def _handle_results(data) -> None:
            print(data)

        return self._create_request(

            Routes.Company.Get(company_id),
            _handle_results

            )
