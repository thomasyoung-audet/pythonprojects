from location import Location, manhattan_distance
from rider import Rider


class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type identifier: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """
        self.identifier = identifier
        self.location = location
        self.speed = speed
        self.destination = None
        self.is_idle = True

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        """
        return 'driver {} at {} going at {} speed'.format(
                self.identifier, self.location, self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        """
        return self.identifier == other.identifier, self.speed == other.speed, \
            self.location == other.location

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        """
        # travel time includes time to pick up rider and drop him off at his
        # destination?
        return round(manhattan_distance(self.location, destination)/self.speed)

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        self.is_idle = False
        self.destination = location

        return round(manhattan_distance(self.location, location)/self.speed)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        self.location = self.destination

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        """

        self.is_idle = False
        self.destination = rider.destination
        return round(manhattan_distance(self.location, rider.destination) /
                     self.speed)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # make driver available again
        self.is_idle = True
        # set self.location to the riders destination
        self.location = self.destination
