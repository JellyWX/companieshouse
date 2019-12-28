class Cache():
    """Singleton class for caching companies and officers. Necessary to form
    connections between officers and companies in a non-wasteful way.

    """

    def __init__(self):
        # Dictionary stores K: V as company_number: Company
        self.all_companies = {}

        # Dictionary stores K: V as officer_route_id: Officer
        self.all_officers = {}

    def create_company(self):
        pass

    def create_officer(self):
        pass
