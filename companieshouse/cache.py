class Cache():
    """Class for caching companies and officers. Necessary to form
    connections between officers and companies in a non-wasteful way.

    """

    def __init__(self):
        # Dictionary stores K: V as company_number: Company
        self._all_companies = {}

        # Dictionary stores K: V as officer_route_id: Officer
        self._all_officers = {}

    def put_company(self, company):
        self._all_companies[company.company_id] = company

    def put_officer(self, officer):
        self._all_officers[officer.officer_id] = officer

    def retrieve_company(self, company_id):
        return self._all_companies.get(company_id, None)

    def retrieve_officer(self, officer_id):
        return self._all_officers.get(officer_id, None)
