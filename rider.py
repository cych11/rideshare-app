"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
WAITING: A constant used for the waiting rider status.
CANCELLED: A constant used for the cancelled rider status.
SATISFIED: A constant used for the satisfied rider status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    """A rider for a ride-sharing service.

    === Public attributes ===
    identifier: The name of the rider
    patience: The amount of time the rider will wait for a driver to pick them
              up prior to cancelling the ride
    origin: Where the rider is waiting to be picked up
    destination: Where the rider wants to be dropped off
    """
    identifier: str
    patience: int
    origin: Location
    destination: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Rider.

        """
        self.identifier = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['location']})
