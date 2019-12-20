from .address import Address

from datetime import datetime
from enum import Enum

class CompanyType(Enum):
    LimitedLiability = 'ltd'

company_types_map = {
    'ltd': CompanyType.LimitedLiability
}

class CompanyStatus(Enum):
    Active = 'active'
    Dissolved = 'dissolved'

company_status_map = {
    'active': CompanyStatus.Active,
    'dissolved': CompanyStatus.Dissolved,

}

class Company():
    def __init__(self,
        title=None, # title of company
        date_of_creation=None, # date company was formed
        company_number=None, # uid for company
        company_status=None, # if company is active or what
        company_type=None, # if company is limited liability or corporated or what
        address=None, # registered company address
        **kwargs # disregard the other arguments (they're mostly useless)
        ):

        self.date_of_creation = datetime.strptime(date_of_creation, '%Y-%m-%d')
        self.company_id = company_number
        self.company_status = company_status_map[company_status]
        self.company_type = company_types_map[company_type]
        self.address = Address(**address)