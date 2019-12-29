from .address import Address

class Officer():
    def __init__(self, querier,
        name=None,
        address=None,
        ,
        **kwargs,
        ):

        self.querier = querier

        self.name = name
        self.address = Address(**address)

        self.officer_id = 
