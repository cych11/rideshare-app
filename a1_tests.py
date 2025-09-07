from location import Location, manhattan_distance, deserialize_location
from container import PriorityQueue
from driver import Driver
from event import DriverRequest, RiderRequest
from rider import Rider
from dispatcher import Dispatcher
import pytest

""" A test suite for assignment 1.
    
    === Files Tested ===
    location
    container
    rider
    driver
    rider
    dispatcher
    
    === Untested Files ===
    event
    monitor
    simulation
    
    TODO:
    - make some attributes private
    - perhaps add some things to rider class
"""


class TestLocation:

    def test_string_representation(self) -> None:
        place = Location(1, 1)  # both positive
        assert str(place) == '1,1'
        place = Location(1, -1)  # one negative
        assert str(place) == '1,-1'
        place = Location(1, 100000000)  # one big
        assert str(place) == '1,100000000'
        place = Location(-1, -2)  # both negative
        assert str(place) == '-1,-2'

    def test_equality(self) -> None:
        place = Location(1, 10)
        place2 = Location(1, 10)
        place3 = Location(4, 5)
        assert place == place2
        assert place == place
        assert place != place3

    def test_manhattan(self) -> None:
        # Test the distance when both locations are the same
        loc1 = Location(0, 0)
        loc2 = Location(0, 0)
        assert manhattan_distance(loc1, loc2) == 0

        # Test the distance when the movement is purely horizontal
        loc1 = Location(0, 0)
        loc2 = Location(0, 5)
        assert manhattan_distance(loc1, loc2) == 5

        # Test the distance when the movement is purely vertical
        loc1 = Location(0, 0)
        loc2 = Location(5, 0)
        assert manhattan_distance(loc1, loc2) == 5

        # Test the distance when the movement is diagonal
        loc1 = Location(0, 0)
        loc2 = Location(3, 4)
        assert manhattan_distance(loc1, loc2) == 7

        # Test the distance when one of the locations has negative coordinates
        loc1 = Location(-1, -2)
        loc2 = Location(3, 4)
        assert manhattan_distance(loc1, loc2) == 10

        # Test the distance when both locations have a mix of positive and
        # negative coordinates
        loc1 = Location(1, -2)
        loc2 = Location(-3, 4)
        assert manhattan_distance(loc1, loc2) == 10

    def test_deserialization(self) -> None:
        # Test deserialization of a normal positive location
        loc_str = "3,4"
        loc = deserialize_location(loc_str)
        assert loc.row == 3
        assert loc.col == 4

        # Test deserialization of a location with zero values
        loc_str = "0,0"
        loc = deserialize_location(loc_str)
        assert loc.row == 0
        assert loc.col == 0

        # Test deserialization of a location with negative values
        loc_str = "-1,-2"
        loc = deserialize_location(loc_str)
        assert loc.row == -1
        assert loc.col == -2

        # Test deserialization of a mixed positive and negative location
        loc_str = "1,-2"
        loc = deserialize_location(loc_str)
        assert loc.row == 1
        assert loc.col == -2

        # Test deserialization of a location with large values
        loc_str = "12345,67890"
        loc = deserialize_location(loc_str)
        assert loc.row == 12345
        assert loc.col == 67890

        # Test deserialization of a location with spaces around the comma
        loc_str = " 7 , 8 "
        loc = deserialize_location(loc_str)
        assert loc.row == 7
        assert loc.col == 8


class TestContainer:

    def test_add_single_item(self):
        pq = PriorityQueue()
        pq.add("red")
        assert pq._items == ["red"]

    def test_add_multiple_items(self):
        pq = PriorityQueue()
        pq.add("yellow")
        pq.add("blue")
        pq.add("red")
        pq.add("green")
        assert pq._items == ["blue", "green", "red", "yellow"]

    def test_add_items_with_same_priority(self):
        pq = PriorityQueue()
        pq.add(2)
        pq.add(1)
        pq.add(1)
        pq.add(3)
        pq.add(2)
        assert pq._items == [1, 1, 2, 2, 3]

    def test_add_and_remove(self):
        pq = PriorityQueue()
        pq.add("yellow")
        pq.add("blue")
        pq.add("red")
        pq.add("green")
        assert pq.remove() == "blue"
        assert pq.remove() == "green"
        assert pq.remove() == "red"
        assert pq.remove() == "yellow"
        assert pq.is_empty()

    def test_add_to_empty_queue(self):
        pq = PriorityQueue()
        pq.add("only_item")
        assert pq._items == ["only_item"]
        assert pq.remove() == "only_item"
        assert pq.is_empty()

    def test_priority_queue_with_floats(self):
        pq = PriorityQueue()
        pq.add(2.3)
        pq.add(1.5)
        pq.add(3.7)
        pq.add(1.8)
        assert pq._items == [1.5, 1.8, 2.3, 3.7]


# some locations, drivers and riders to be used
locations = [Location(1, 1), Location(2, 2), Location(3, 3), Location(4, 4)]


@pytest.fixture
def driver1():
    return Driver('D1', locations[0], 1)


@pytest.fixture
def driver2():
    return Driver('D2', locations[1], 1)


@pytest.fixture
def driver3():
    return Driver('D3', locations[2], 1)


@pytest.fixture
def rider1():
    return Rider('R1', 100, locations[0], locations[3])


@pytest.fixture
def rider2():
    return Rider('R2', 100, locations[1], locations[3])


@pytest.fixture
def rider3():
    return Rider('R3', 100, locations[2], locations[3])


@pytest.fixture
def dispatcher():
    return Dispatcher()


class TestPriorityContainerReal:

    def test_add_event_different_timestamps(self, driver1, driver2, driver3, rider1, rider2, rider3):
        eq = PriorityQueue()
        req1 = RiderRequest(1, rider1)
        req2 = RiderRequest(2, rider2)
        req3 = RiderRequest(3, rider3)
        req4 = DriverRequest(1, driver1)
        req5 = DriverRequest(2, driver2)
        req6 = DriverRequest(3, driver3)
        lst = [req1, req2, req3, req4, req5, req6]
        for event in lst:
            eq.add(event)
        assert eq._items == [req4, req1, req5, req2, req6, req3]

    def test_priority_order(self, driver1, driver2, driver3, rider1, rider2, rider3):
        eq = PriorityQueue()
        req1 = RiderRequest(1, rider1)
        req2 = RiderRequest(1, rider2)
        req3 = RiderRequest(1, rider3)
        req4 = DriverRequest(1, driver1)
        req5 = DriverRequest(1, driver2)
        req6 = DriverRequest(1, driver3)
        lst = [req1, req2, req3, req4, req5, req6]
        for event in lst:
            eq.add(event)
        assert eq._items == [req4, req5, req6, req1, req2, req3]

    def test_remove_event(self, driver1, rider1):
        eq = PriorityQueue()
        req1 = RiderRequest(1, rider1)
        req2 = DriverRequest(0, driver1)
        eq.add(req1)
        eq.add(req2)
        assert eq.remove() == req2
        assert eq.remove() == req1

    def test_is_empty(self, driver1):
        eq = PriorityQueue()
        assert eq.is_empty()
        req1 = DriverRequest(0, driver1)
        eq.add(req1)
        assert not eq.is_empty()
        eq.remove()
        assert eq.is_empty()


class TestDriver:
    def test_driver_initialization(self, driver1):
        assert driver1.id == 'D1'
        assert driver1.location == locations[0]
        assert driver1.speed == 1
        assert driver1.is_idle
        assert driver1.destination is None

    def test_driver_str(self, driver1, driver2, driver3):
        assert str(driver1) == 'D1'
        assert str(driver2) == 'D2'
        assert str(driver3) == 'D3'

    def test_driver_eq(self, driver1, driver2):
        driver1_copy = Driver('D1', locations[0], 1)

        assert driver1 == driver1_copy
        assert driver1 != driver2

    def test_get_travel_time(self, driver1):
        travel_time = driver1.get_travel_time(locations[3])
        expected_time = 6

        assert travel_time == expected_time

    def test_start_drive(self, driver1):
        travel_time = driver1.start_drive(locations[3])
        expected_time = 6

        assert travel_time == expected_time
        assert driver1.destination == locations[3]
        assert not driver1.is_idle

    def test_end_drive(self, driver1):
        driver1.start_drive(locations[3])
        driver1.end_drive()

        assert driver1.location == locations[3]

    def test_start_ride(self, driver1, rider1):
        travel_time = driver1.start_ride(rider1)
        expected_time = round(manhattan_distance(locations[0],
                                                 locations[3]) / driver1.speed)

        assert travel_time == expected_time
        assert driver1.destination == locations[3]

    def test_end_ride(self, driver1, rider1):
        driver1.start_ride(rider1)
        driver1.end_ride()


class TestDispatcher:

    def test_dispatcher_initialization(self, dispatcher):
        assert dispatcher._driver_list == []
        assert dispatcher._rider_list == []

    def test_request_driver_with_no_drivers(self, dispatcher, rider1):
        assigned_driver = dispatcher.request_driver(rider1)

        assert assigned_driver is None
        assert dispatcher._rider_list == [rider1]

    def test_request_driver_with_available_drivers(self, dispatcher, driver1,
                                                   driver2, driver3, rider1):
        dispatcher._driver_list = [driver1, driver2, driver3]

        assigned_driver = dispatcher.request_driver(rider1)

        assert assigned_driver == driver1
        assert dispatcher._rider_list == []

    def test_request_driver_with_no_idle_drivers(self, dispatcher, driver1,
                                                 driver2, rider1):
        driver1.is_idle = False
        driver2.is_idle = False
        dispatcher.drivers = [driver1, driver2]

        assigned_driver = dispatcher.request_driver(rider1)

        assert assigned_driver is None
        assert dispatcher._rider_list == [rider1]

    def test_request_rider_with_no_riders(self, dispatcher, driver1):
        dispatcher.drivers = [driver1]

        assigned_rider = dispatcher.request_rider(driver1)

        assert assigned_rider is None
        assert dispatcher.drivers == [driver1]

    def test_request_rider_with_waiting_riders(self, dispatcher, driver1,
                                               rider1, rider2):
        dispatcher._rider_list = [rider1, rider2]

        assigned_rider = dispatcher.request_rider(driver1)

        assert assigned_rider == rider1
        assert dispatcher._rider_list == [rider2]

    def test_cancel_ride(self, dispatcher, rider1, rider2):
        dispatcher._rider_list = [rider1, rider2]

        dispatcher.cancel_ride(rider1)

        assert dispatcher._rider_list == [rider2]
        assert rider1.status == 'cancelled'

    def test_register_new_driver(self, dispatcher, driver1):
        assert driver1 not in dispatcher._driver_list

        dispatcher.request_rider(driver1)

        assert driver1 in dispatcher._driver_list


class TestDispatcherReqDriver:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Setup dispatcher, locations, drivers, and riders before each test
        # i need to change locations so a rider may be closer to a driver
        # but their speed is slower so you should get the faster guy
        self.dispatcher = Dispatcher()
        self.locations = [Location(1, 10), Location(1, 20),
                          Location(1, 30), Location(1, 40)]
        self._driver_list = [
            Driver('D1', self.locations[3], 30),
            Driver('D2', self.locations[1], 1),
            Driver('D3', self.locations[2], 5),
        ]
        self._rider_list = [
            Rider('R1', 100, self.locations[0], self.locations[3]),
            Rider('R2', 100, self.locations[1], self.locations[3]),
            Rider('R3', 100, self.locations[2], self.locations[3]),
            Rider('R4', 100, self.locations[3], self.locations[3])
        ]

    def test_request_driver_no_drivers(self):
        # No drivers available
        assigned_driver = self.dispatcher.request_driver(self._rider_list[0])
        assert assigned_driver is None
        assert self.dispatcher._rider_list == [self._rider_list[0]]

    def test_request_driver_with_available_drivers(self):
        # Add drivers to the dispatcher
        self.dispatcher._driver_list.extend(self._driver_list)

        # Assign a driver to rider1 (should be driver1)
        # rider is at (1, 10)
        # driver1 is a (1, 40) with speed 30 and would take 1 time to get there
        # driver 2 is at (1, 20) with speed 1 and should take 10 time to arrive
        # driver 3 is at (1, 30) with speed 5 and should take 0.5 time
        assigned_driver = self.dispatcher.request_driver(self._rider_list[0])
        assert assigned_driver == self._driver_list[0]
        assert self.dispatcher._rider_list == []

        # change driver1 so they're not available
        self._driver_list[0].is_idle = False

        # rider 1 is at (1, 20)
        # driver 2 should be assigned, already at the location
        assigned_driver = self.dispatcher.request_driver(self._rider_list[1])
        assert assigned_driver == self._driver_list[1]
        assert self.dispatcher._rider_list == []

        # change driver2 so they're not available
        self._driver_list[1].is_idle = False

        # only one driver left, should be driver 3
        assigned_driver = self.dispatcher.request_driver(self._rider_list[2])
        assert assigned_driver == self._driver_list[2]
        assert self.dispatcher._rider_list == []

        # change driver 3 so they're not available
        self._driver_list[2].is_idle = False

        # now request a driver for the last rider with no available driver
        assigned_driver = self.dispatcher.request_driver(self._rider_list[3])
        assert assigned_driver is None
        assert self.dispatcher._rider_list == [self._rider_list[3]]

    def test_request_driver_with_idle_driver_becoming_available(self):
        # tbh don't know if this scenario would ever happen
        # Add drivers to the dispatcher and set them as busy
        self.dispatcher._driver_list.extend(self._driver_list)
        for driver in self._driver_list:
            driver.is_idle = False

        # Request a driver for rider1 (should be in waiting list, no drivers)
        assigned_driver = self.dispatcher.request_driver(self._rider_list[0])
        assert assigned_driver is None
        assert self.dispatcher._rider_list == [self._rider_list[0]]

        # Set driver1 to idle and closest to rider1
        self._driver_list[0].is_idle = True
        self._driver_list[0].location = self.locations[0]

        # Request a driver for rider1 again (should assign driver1)
        assigned_driver = self.dispatcher.request_driver(self._rider_list[0])
        assert assigned_driver == self._driver_list[0]
        assert self.dispatcher._rider_list == []


if __name__ == '__main__':
    pytest.main(['a1_tests.py'])
