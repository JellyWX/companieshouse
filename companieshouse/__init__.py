from enum import IntEnum
import requests
from typing import Optional
from .search_result import SearchResults

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
    pass

class InvalidAuthToken(Exception):
    pass

class InvalidIPOrDomain(Exception):
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

    def new_search(self, query: str) -> SearchResults:
        return SearchResults(query)

    # Function turns search query into request, sends request, converts request into search result
    def search_for(self, query: str, search_type=SearchType.Company | SearchType.Officer, page_size: Optional[int]=None) -> Optional[SearchResults]:

        def _handle_error(request):
            if request.status_code == 401:
                raise BadRequest

            elif request.status_code == 403:
                if request.text == '':
                    raise InvalidIPOrDomain('Either your IP address does not match the IP on your application or you haven\'t added `https://local.sender` as a JavaScript domain')

                else:
                    raise InvalidAuthToken

            elif request.status_code == 500:
                raise InternalServerError

        def _handle_results(data, query) -> SearchResults:
            search_results = data['items']

            print(search_results)

            result_count: int = data['total_results']
            items_per_page: int = data['items_per_page']

            s = SearchResults.from_first_page(query, result_count, items_per_page, search_results)

            return s

        request = requests.get('{}?q={}'.format(Routes.Search[search_type], query), auth=(self._auth_token, ''), headers={'Origin': 'https://local.sender'})

        if request.status_code != 200:
            _handle_error(request)

        else:
            data = request.json()

            return _handle_results(data)
