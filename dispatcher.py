"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    # === Private Attributes ===
    _driver_list: list
    #     All available drivers waiting for a rider
    _rider_list: list

    #     All riders that have requested a driver
    #
    # === Representation Invariants ===
    # driver_list and rider_list are sorted, where the first item in the list
    # is the item with the highest priority.

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self._driver_list = []
        self._rider_list = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return (f'Available Drivers: {self._driver_list}, '
                f'Available Riders: {self._rider_list}')

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.
        """
        curr_min = 10000000000
        curr_driver = None
        # iterate over all the drivers and see which ones are currently idle
        for driver in self._driver_list:
            if driver.is_idle:
                # if the driver is idle, get the time it takes for that driver
                # to arrive to the rider and if it is lower than the curr_min,
                # set the currently assigned driver to that driver and replace
                # the curr_min value to the travel time
                driver_time = driver.get_travel_time(rider.origin)
                if curr_min > driver_time:
                    curr_min = driver_time
                    curr_driver = driver
        if curr_driver is not None:
            if rider in self._rider_list:
                self._rider_list.remove(rider)
            return curr_driver  # if there was an available driver, return it
        self._rider_list.append(rider)
        # otherwise there wasn't any available drivers, so the rider will wait
        # in the rider wait list, then return None
        return None

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        """
        # register the driver if it is not in the driver list
        if driver not in self._driver_list:
            self._driver_list.append(driver)
        # if there are no riders waiting for a driver, return None
        if len(self._rider_list) == 0:
            return None
        # since the if statement was not executed, there is a rider waiting to
        # be picked up, so remove them from the wait list and have the driver
        # begin the pickup event for the rider, returning the rider
        rider = self._rider_list.pop(0)
        driver.start_drive(rider.origin)
        return rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        """
        if rider in self._rider_list:
            self._rider_list.remove(rider)
        rider.status = "cancelled"


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
