class SearchResults():
    def __init__(self, query):
        self.query = query
        self.result_count = -1
        self.items_per_page = 20
        self.current_page = 0

        self.officers = []
        self.companies = []

    def _add_company(self, company: Company):
        self.companies.append(company)

    def _add_officer(self, officer: Officer):
        self.officers.append(officer)

    @staticmethod
    def from_first_page(query, result_count, items_per_page, search_results):
        s = SearchResults(query)

        s.result_count = result_count
        s.items_per_page = items_per_page
        s.current_page = 1

        for item in search_results:
            if item['kind'] == 'searchresults#company':
                s._add_company(Company(item))

            else:
                s._add_officer(Officer(item))
