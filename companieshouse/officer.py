from .address import Address

class Officer():
    def __init__(self, querier,
        name=None,
        address=None,
        appointment_count=None,
        **kwargs,
        ):

        self.querier = querier

        self.title = name
        self.appointment_count = appointment_count
        self.address = Address(**address)
