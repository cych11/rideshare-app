"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    === Public attributes ===
    row: number of blocks the location is from the bottom edge of the grid
    col: number of blocks the location is from the left of the grid
    """
    row: int
    col: int

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.

        """
        self.row = row
        self.col = column

    def __str__(self) -> str:
        """Return a string representation.

        """
        return str(self.row) + "," + str(self.col)

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        return self.row == other.row and self.col == other.col


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.

    """
    # calculate the absolute difference of the origin and destinations x value
    horizontal_distance = abs(destination.row - origin.row)
    # calculate the absolute difference of the origin and destinations y value
    vertical_distance = abs(destination.col - origin.col)
    # manhattan_distance is the horizontal and vertical distances added
    return horizontal_distance + vertical_distance


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'
    """
    # split the location_str in 2, where index 0 is the x value, index 1 is the
    # y value.
    split_string = location_str.split(",")
    return Location(int(split_string[0]),
                    int(split_string[1]))


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
