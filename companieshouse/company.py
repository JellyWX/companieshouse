from .address import Address
from .search_result import OfficerList

from datetime import datetime
from enum import Enum

class CompanyType(Enum):
    LimitedLiability = 'ltd'
    UKEstablishment = 'uk-establishment'
    OverseaCompany = 'oversea-company'

    @classmethod
    def from_string(cls, t):

        company_types_map = {
            'ltd': cls.LimitedLiability,
            'uk-establishment': cls.UKEstablishment,
            'oversea-company': cls.OverseaCompany,
        }

        return company_types_map[t]


class CompanyStatus(Enum):
    Active = 'active'
    Dissolved = 'dissolved'
    Closed = 'closed'
    ClosedOn = 'closed-on'

    @classmethod
    def from_string(cls, t):

        company_status_map = {
            'active': cls.Active,
            'dissolved': cls.Dissolved,
            'closed': cls.Closed,
            'closed-on': cls.ClosedOn,
        }

        return company_status_map[t]

class Company():
    def __init__(self, querier,
        title=None, # title of company
        company_name=None,

        date_of_creation=None, # date company was formed
        
        company_number=None, # uid for company
        
        company_status=None, # if company is active or what
        status=None,
        
        company_type=None, # if company is limited liability or corporated or what
        type=None,
        
        address=None, # registered company address
        registered_office_address=None,
        
        **kwargs # disregard the other arguments (they're mostly useless)
        ):

        self.querier = querier

        self.title = title or company_name
        self.date_of_creation = datetime.strptime(date_of_creation, '%Y-%m-%d')
        self.company_id = company_number
        self.company_status = CompanyStatus.from_string(company_status or status)
        self.company_type = CompanyType.from_string(company_type or type)

        self.officers = OfficerList(self, querier)

        address = address or registered_office_address

        if address.get('locality') == 'Refer To Parent Registry':
            self.address = Address()

        else:
            self.address = Address(**address)
