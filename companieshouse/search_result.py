from .company import Company
from .officer import Officer

class Page():
    def __init__(self, search_results):
        self.entities = []

        for item in search_results:
            if item['kind'] == 'searchresults#company':
                self._add_entity(Company(**item))

            else:
                self._add_entity(Officer(**item))

    def __getitem__(self, index):
        return self.entities[index]

    def _add_entity(self, entity):
        self.entities.append(entity)


class Search():
    def __init__(self, query, query_type, querier):
        self._PAGE_SIZE = 15
        self.query = query
        self.query_type = query_type
        self.querier = querier

        self.pages = {}

    def __getitem__(self, index):
        page_required, item_required = divmod(index, self._PAGE_SIZE)

        page = self.get_page(page_required)

        return page[item_required]

    def __iter__(self):
        pass

    def get_page(self, page_number):
        if self.pages.get(page_number, None) is None:
            p = self.get_upstream_page(page_number)

            self.pages[page_number] = p
            return p

        else:
            return self.pages[page_number]

    def get_upstream_page(self, page_number) -> Page:
        return self.querier.get_search_page(self.query, self.query_type, self._PAGE_SIZE, self._PAGE_SIZE * page_number)

