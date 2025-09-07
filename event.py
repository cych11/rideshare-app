"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from __future__ import annotations
from typing import List
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
    timestamp: A timestamp for this event.
    """

    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

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

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    rider: The rider.
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a RiderRequest event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def __str__(self) -> str:
        """
        Return a string representation of a RiderRequest, containing the name
        of the event, the time, and who the rider is
        """
        return "{} -- {}: Request a driver at {} to {}".format(
            self.timestamp, self.rider.identifier, self.rider.origin,
            self.rider.destination)

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        """
        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.identifier, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)
        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 driver, self.rider))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))
        return events


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    driver: The driver.
    """

    driver: Driver

    def __init__(self, timestamp: int, driver: Driver) -> None:
        """Initialize a DriverRequest event.

        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        """
        # Notify the monitor about the request.
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)
        events = []
        # Request a rider from the dispatcher.
        rider = dispatcher.request_rider(self.driver)
        if rider is not None:
            # If there is one available, the driver starts driving towards the
            # rider, and the method returns a Pickup event for when the driver
            # arrives at the rider's location.
            travel_time = self.driver.start_drive(rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.driver, rider))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {}: Request a rider at {}".format(
            self.timestamp, self.driver.id, self.driver.location)


class Cancellation(Event):
    """A rider requests to cancel their pickup event.

    Precondition: rider's current status is WAITING

    === Attributes ===
    rider: The rider.
    """

    rider: Rider

    def __init__(self, timestamp: int, rider: Rider) -> None:
        """Initialize a Cancellation event.

        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """Changes a waiting rider to a cancelled rider, and doesn't
        schedule any future events.
        """
        # If the rider is not satisfied and thus is still waiting by the time
        # that the cancellation event is occurring, notify the monitor of the
        # cancellation, set the riders status as cancelled, and have the
        # dispatcher remove them from the rider wait list if they are still in
        # the wait list.
        if self.rider.status != SATISFIED:
            monitor.notify(self.timestamp, RIDER, CANCEL,
                           self.rider.identifier, self.rider.origin)
            self.rider.status = CANCELLED
            dispatcher.cancel_ride(self.rider)
        return []

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {}: Cancelled".format(self.timestamp,
                                            self.rider.identifier)


class Pickup(Event):
    """
    A driver is sent to a rider's location, picks them up, and drives the rider
    to their desired destination.

    === Attributes ===
    driver: The driver.
    rider: The rider.
    """

    driver: Driver
    rider: Rider

    def __init__(self, timestamp: int, driver: Driver, rider: Rider) -> None:
        """Initialize a Pickup event.

        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        The driver arrives at the riders origin and if the rider has not
        cancelled yet, the rider will be picked up where a dropoff event is
        scheduled. Otherwise, if the rider has cancelled, the driver will
        request a new rider once they arrive at the cancelled rider's origin.
        """
        self.driver.end_drive()  # have the driver arrive at the riders origin
        # notify the monitor that the pickup is happening
        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.id, self.driver.location)
        events = []
        if self.rider.status == WAITING:
            # if the rider is waiting, have the driver pickup the rider and
            # begin driving to the riders destination
            travel_time = self.driver.start_ride(self.rider)
            # notify the monitor that the rider has been picked up
            monitor.notify(self.timestamp, RIDER, PICKUP,
                           self.rider.identifier, self.rider.origin)
            # change the riders status to satisfied
            self.rider.status = SATISFIED
            # notify the monitor that the rider will be dropped off
            events.append(Dropoff(self.timestamp + travel_time, self.driver,
                                  self.rider))
        # if the rider has cancelled, have the driver request a new rider
        elif self.rider.status == CANCELLED:
            events.append(DriverRequest(self.timestamp, self.driver))
        return events

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {} picked up {} at {}".format(
            self.timestamp, self.driver.id, self.rider.identifier,
            self.driver.destination)


class Dropoff(Event):
    """
    A driver goes to the riders desired destination, drops them off, and begins
    to request another pickup after

    === Attributes ===
    driver: The driver.
    rider: The rider.
    """

    driver: Driver
    rider: Rider

    def __init__(self, timestamp: int, driver: Driver, rider: Rider) -> None:
        """Initialize a Dropoff event.

        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher: Dispatcher, monitor: Monitor) -> List[Event]:
        """
        A dropoff event sets the driver’s location to the rider’s destination.
        The driver needs more work, so a new event for the driver requesting a
        rider is scheduled to take place immediately, and the driver has no
        destination for the moment
        """
        self.driver.end_ride()  # have the driver arrive at the destination
        # notify the monitor that both the driver and rider have completed
        # their drop-off event
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.id, self.driver.location)
        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.identifier, self.rider.destination)
        # the driver then requests a new rider after the drop-off
        return [DriverRequest(self.timestamp, self.driver)]

    def __str__(self) -> str:
        """Return a string representation of this event.

        """
        return "{} -- {} dropped off {} at {}".format(
            self.timestamp, self.driver.id, self.rider.identifier,
            self.driver.destination)


def create_event_list(filename: str) -> List[Event]:
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    filename: The name of a file that contains the list of events.
    """
    events = []
    drivers = {}
    riders = {}
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
            event = None

            # HINT: Use Location.deserialize to convert the location string to
            # a location.

            if event_type == "DriverRequest":
                # Create a DriverRequest event.
                if tokens[2] in drivers:
                    event = DriverRequest(timestamp, drivers[tokens[2]])
                else:
                    # initialize the driver
                    drivers[tokens[2]] = Driver(tokens[2],
                                                deserialize_location
                                                (tokens[3]),
                                                int(tokens[4]))
                    # Create a DriverRequest event.
                    event = DriverRequest(timestamp, drivers[tokens[2]])
            elif event_type == "RiderRequest":
                # Create a RiderRequest event.
                if tokens[2] in riders:
                    event = RiderRequest(timestamp, riders[tokens[2]])
                else:
                    # initialize the rider
                    riders[tokens[2]] = Rider(tokens[2],
                                              int(tokens[5]),
                                              deserialize_location
                                              (tokens[3]),
                                              deserialize_location
                                              (tokens[4]))
                    # Create a RiderRequest event.
                    event = RiderRequest(timestamp, riders[tokens[2]])

            events.append(event)

    return events


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'allowed-io': ['create_event_list'],
            'extra-imports': ['rider', 'dispatcher', 'driver',
                              'location', 'monitor']})
