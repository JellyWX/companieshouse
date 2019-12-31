from .address import Address

class Officer():
    def __init__(self, querier,
        name=None,
        address=None,
        links=None,
        **kwargs,
        ):

        self.querier = querier

        self.name = name
        self.address = Address(**address)

        self.officer_id = links['officer']['appointments'][len('/officers/'):-len('/appointments')]

        self.appointments = AppointmentList(self.querier)
