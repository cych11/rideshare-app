from location import Location, manhattan_distance, deserialize_location
from container import Container, PriorityQueue
from rider import Rider
from driver import Driver
from dispatcher import Dispatcher


def test_location_init() -> None:
    """
    Initializing a location, ensuring that the coordinates and string
    representation are correctly set.
    """
    location1 = Location(1,1)
    assert str(location1) == "1,1"


def test_location_eq() -> None:
    """
    Check that 2 of the same or different locations are correctly determined
    if they are equal or not
    """
    location1 = Location(1, 1)
    location2 = Location(3, 3)
    location3 = Location(3, 3)
    location4 = Location(3, 4)
    assert location1 != location3
    assert location2 == location3
    assert location3 == location3
    assert location3 != location4


def test_manhattan_distance() -> None:
    """
    Test that the manhattan distance of many different coordinates
    """
    location1 = Location(1, 1)
    location2 = Location(3, 3)
    location3 = Location(3, 3)
    location4 = Location(3, 8)
    assert manhattan_distance(location1, location1) == 0
    assert manhattan_distance(location1, location2) == 4
    assert manhattan_distance(location2, location1) == 4
    assert manhattan_distance(location2, location3) == 0
    assert manhattan_distance(location2, location4) == 5


def test_priority_queue() -> None:
    """
    Test
    """
    pass


def test_rider() -> None:
    """
    Test
    """
    pass


def test_driver() -> None:
    """
    Test for functionality of the Driver class
    """
    location1 = Location(1, 1)
    location2 = Location(3, 3)
    location3 = Location(3, 8)
    driver = Driver("bob", location1, 1)
    driver2 = Driver("bobby", location2, 1)
    driver3 = Driver("bob", location2, 2)
    assert str(driver) == "bob 1,1 1"
    assert driver != driver2
    assert driver == driver
    assert driver != driver3
    rider = Rider("megan", 10, location2, location3)
    assert driver.location == location1
    assert rider.origin == location2
    assert driver.is_idle is True
    assert driver.start_drive(rider.origin) == 4
    assert driver.is_idle is False
    driver.end_drive()
    assert driver.is_idle is True
    assert driver.location == rider.origin
    assert driver.start_ride(rider) == 5
    assert driver.is_idle is False
    driver.end_ride()
    assert driver.is_idle is True
    assert driver.location == location3 and driver.destination is None


