"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:
    """
    A rider for a ride-share service

    Attributes
    ==========
    @type id: str
        A unique identifier for this Rider
    @type origin: Location
        the starting Location of the Rider
    @type destination: Location
        the Location of the Rider's destination
    @type status: str
        the current status of the Rider (Waiting, Cancelled or Satisfied)
    @type patience: int
        the amount of time units the Rider will wait before cancellation
    """
    def __init__(self, identifier, origin, destination, patience):
        """
        Create a Rider
        @type identifier: str
        @type origin: Location
        @type destination: Location
        @type patience: int
        @rtype: None
        """
        self.id = identifier
        self.origin = origin
        self.destination = destination
        self.patience = patience
        self.status = WAITING

    def __eq__(self, other):
        """

        @type self = Rider
        @type other = Rider
        @rtype = bool
        """
        return (self.id == other.id and self.origin == other.origin and
                self.destination == other.destination and
                self.patience == other.patience)
