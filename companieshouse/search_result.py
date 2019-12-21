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
        if index >= len(self):
            return None

        else:
            return self.entities[index]

    def __len__(self):
        return len(self.entities)

    def _add_entity(self, entity):
        self.entities.append(entity)


class Search():
    def __init__(self, query, query_type, querier):
        self._PAGE_SIZE = 15

        self.result_count = 0

        self.query = query
        self.query_type = query_type
        self.querier = querier

        self.pages = {}

        self.iter_head = 0

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError

        else:
            page_required, item_required = divmod(index, self._PAGE_SIZE)

            page = self.get_page(page_required)

            return page[item_required]

    def __iter__(self):
        self.iter_head = 0
        return self

    def __next__(self):
        if self.iter_head >= len(self):
            raise StopIteration

        else:
            a = self[self.iter_head]
            self.iter_head += 1

            return a

    def __len__(self):
        return self.result_count

    def get_page(self, page_number):
        if self.pages.get(page_number, None) is None:
            p = self.get_upstream_page(page_number) or Page([])

            self.pages[page_number] = p
            return p

        else:
            return self.pages[page_number]

    def get_upstream_page(self, page_number) -> Page:
        page, result_count = self.querier.get_search_page(self.query, self.query_type, self._PAGE_SIZE, self._PAGE_SIZE * page_number)

        if result_count != self.result_count:
            print('Results have changed; deleting cache')
            # results have changed! delete all existing pages :(
            self.pages = {}

        self.result_count = result_count

        return page
