import logging

class Page():
    def __init__(self, search_results):
        self.entities = []

        for item in search_results:
            self._add_entity(Company(querier, **item))

    def __getitem__(self, index):
        if index >= len(self):
            return None

        else:
            return self.entities[index]

    def __len__(self):
        return len(self.entities)

    def _add_entity(self, entity):
        self.entities.append(entity)


class OfficerListPage(Page):
    def __init__(self, search_results):
        self.entities = []

        for item in search_results:
            self._add_entity(Officer(querier, **item))


class Search():
    def __init__(self, query, querier):
        self._PAGE_SIZE = 15

        self.result_count = 0

        self.query = query
        self.querier = querier

        self.pages = {}

        self.iter_head = 0

    def __getitem__(self, index):
        if len(self) != 0 and index >= len(self):
            raise IndexError

        else:
            page_required, item_required = divmod(index, self._PAGE_SIZE)

            page = self.get_page(page_required)

            return page[item_required]

    def __iter__(self):
        self.iter_head = 0
        return self

    def __next__(self):
        if len(self) != 0 and self.iter_head >= len(self):
            raise StopIteration

        else:
            a = self[self.iter_head]
            self.iter_head += 1

            return a

    def __len__(self):
        return self.result_count

    def get_page(self, page_number):
        if self.pages.get(page_number, None) is None:
            p = self._get_upstream_page(page_number) or Page([])

            self.pages[page_number] = p
            return p

        else:
            return self.pages[page_number]

    def _get_upstream_page(self, page_number) -> Page:
        logging.info('Requesting new search page from upstream')

        page, result_count = self.querier.get_search_page(self.query, self._PAGE_SIZE, self._PAGE_SIZE * page_number)

        self._validate_result_count(result_count)

        return page

    def _validate_result_count(self, result_count):

        if result_count != self.result_count:
            logging.info('Results have changed; deleting cache')
            self.pages = {}

        self.result_count = result_count


class OfficerList(Search):
    def __init__(self, company, querier):
        self._PAGE_SIZE = 15

        self.result_count = 0

        self.company = company
        self.querier = querier

        self.pages = {}

        self.iter_head = 0

    def _get_upstream_page(self, page_number) -> Page:
        logging.info('Requesting new page of officers from upstream')

        page, result_count = self.querier.get_officer_list_page(self.company.company_id, self._PAGE_SIZE, self._PAGE_SIZE * page_number)

        self._validate_result_count(result_count)

        return page

from .company import Company
from .officer import Officer