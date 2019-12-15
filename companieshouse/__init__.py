from enum import IntEnum
import requests
from typing import Optional

__name__ = 'companieshouse'
__version__ = '0.1'


# API routes
class Routes():
    """Internal usage only

    """

    # Base URI for querying to
    BASE_URI = 'https://api.companieshouse.gov.uk'

    class Search():
        class InvalidSearchType(Exception):
            pass

        All = BASE_URI + '/search'
        Company = BASE_URI + '/search/companies'
        Officer = BASE_URI + '/search/officers'

        def __getitem__(self, index):
            if isinstance(index, int) and 1 <= index <= 3
                return (Company, Officer, All).get(index - 1)

            else:
                raise InvalidSearchType

    class Company():
        Get = BASE_URI + '/company'


class InternalServerError(Exception):
    pass

class InvalidAuthToken(Exception):
    pass

class DomainNotSetOrOther(Exception):
    pass

class BadRequest(Exception):
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

    def __init__(self, auth_token: str):
        self._auth_token = auth_token

    def new_search(self, query: str):
        return SearchResults(query)

    # Function turns search query into request, sends request, converts request into search result
    def search_for(self, query: str, search_type=SearchType.Company | SearchType.Officer, page_size: Optional[int]=None):

        def _handle_error(request):
            if request.status == 401:
                raise BadRequest

            elif request.status == 403:
                if request.text == '':
                    raise DomainNotSetOrOther

                else:
                    raise InvalidAuthToken

            elif request.status == 500:
                raise InternalServerError

        def _handle_results(data, query):
            search_results = data['items']

            result_count: int = data['total_results']
            items_per_page: int = data['items_per_page']

            s = SearchResults.from_first_page(query, result_count, items_per_page, search_results)

            return s

        request = requests.get('{}?q={}'.format(Routes.Search[search_type], query), auth=(self._auth_token, ''), headers={'Origin': 'https://local.sender'})

        if request.status != 200:
            _handle_error(request)

        else:
            data = request.json()

            return _handle_results(data)
