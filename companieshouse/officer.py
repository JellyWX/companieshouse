from .address import Address

class Officer():
    def __init__(self, 
        title=None,
        address=None,
        appointment_count=None,
        **kwargs,
        ):
        
        self.title = title
        self.appointment_count = appointment_count
        self.address = Address(**address)