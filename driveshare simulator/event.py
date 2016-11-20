"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self < other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self <= other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time, self.rider,
                                 driver))
        events.append(Cancellation(self.timestamp + self.rider.patience, self.
                                   rider))
        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """

        if len(dispatcher.driver_list) == 0:
            dispatcher.driver_list.append(self.driver)

        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.identifier, self.driver.location)

        # Request a rider from the dispatcher.
        events = []
        rider = dispatcher.request_rider(self.driver)
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        if rider is not None:
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time, rider,
                                 self.driver))
            self.driver.location = rider.origin
            return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):

    def __init__(self, timestamp, rider):
        """Initialize a Cancellation event.

        @type self: Cancellation
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Changes a waiting rider to a cancelled rider.

        If a rider has already been picked up he is satisfied and can't cancel

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """

        if self.rider.status != SATISFIED:
            dispatcher.cancel_ride(self.rider)
            self.rider.status = CANCELLED

            monitor.notify(self.timestamp, RIDER, CANCEL, self.rider.id,
                           self.rider.origin)

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        return "rider {} has cancelled".format(self.rider.id)


class Pickup(Event):

    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """
        Sets the drivers location to the riders location. If the rider is
        waiting, a ride starts and the drivers destination becomes the riders
        destination.
        A Dropoff event is scheduled for when they arrive at the riders
        destination and the rider becomes satisfied.

        If the rider cancelled the driver requests a new rider and the driver
        destination is None.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """
        self.driver.end_drive()
        events = []

        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.identifier, self.driver.location)

        if self.rider.status != CANCELLED:

            # Start the ride
            ride_time = self.driver.start_ride(self.rider)
            self.rider.status = SATISFIED
            if self.rider in dispatcher.rider_list:
                dispatcher.rider_list.remove(self.rider)

            # Create a new dropoff event
            events.append(Dropoff(self.timestamp+ride_time, self.rider,
                                  self.driver))
            # Report to monitor
            monitor.notify(self.timestamp, RIDER, PICKUP,
                           self.rider.id, self.driver.location)

        else:
            self.driver.destination = None
            self.driver.is_idle = True
            events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """
        if self.rider.status != CANCELLED:
            return "driver {} picked up {} at {}".format\
                (self.driver.identifier, self.rider.id, self.timestamp)
        return "rider {} cancelled before he could be picked up by {}".format\
            (self.rider.id, self.driver.identifier)


class Dropoff(Event):

    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff event

        @type self: Dropoff
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Set driver location to rider destination, leaves rider satisfied.
        Driver requests a new rider and his destination is set to None.

        @type self: Pickup
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: None
        """
        self.driver.end_ride()
        self.driver.destination = None
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.identifier, self.driver.location)
        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.id, self.driver.location)

        events = list()
        events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Dropoff
        @rtype: str
        """
        return "driver {} dropped off rider {} at {}".format\
        (self.driver.identifier, self.rider.id, self.timestamp)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """

    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":

                # Create a DriverRequest event.
                driver_id = tokens[2]
                location_id = deserialize_location(tokens[3])
                speed_id = int(tokens[4])
                driver = Driver(driver_id, location_id, speed_id)
                event = DriverRequest(timestamp, driver)

            elif event_type == "RiderRequest":

                # Create a RiderRequest event.
                rider_id = tokens[2]
                origin_id = deserialize_location(tokens[3])
                destination_id = deserialize_location(tokens[4])
                patience_id = int(tokens[5])
                rider = Rider(rider_id, origin_id, destination_id, patience_id)
                event = RiderRequest(timestamp, rider)

            events.append(event)

    return events
