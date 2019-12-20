class Address():
    def __init__(self, 
        address_line_1=None,
        address_line_2=None,
        care_of_name=None,
        country=None,
        locality=None,
        premises=None,
        **kwargs,
        ):
        
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.owner_of_premises = care_of_name
        self.region = locality
        self.premises = premises
        self.country = country