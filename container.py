"""Containers of objects"""


class Container:
    """A container that holds objects.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def add(self, item: object) -> None:
        """Add <item> to this Container.

        """
        raise NotImplementedError("Implemented in a subclass")

    def remove(self) -> object:
        """Remove and return a single item from this Container.

        """
        raise NotImplementedError("Implemented in a subclass")

    def is_empty(self) -> bool:
        """Return True iff this Container is empty.

        """
        raise NotImplementedError("Implemented in a subclass")


class PriorityQueue(Container):
    """A queue of items that operates in priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first. Ties are resolved in FIFO order,
    meaning the item which was inserted *earlier* is the first one to be
    removed.

    Priority is defined by the rich comparison methods for the objects in the
    container (__lt__, __le__, __gt__, __ge__).

    If x < y, then x has a *HIGHER* priority than y.

    All objects in the container must be of the same type.
    """

    # === Private Attributes ===
    _items: list
    #     The items stored in the priority queue.
    #
    # === Representation Invariants ===
    # _items is a sorted list, where the first item in the queue is the
    # item with the highest priority.

    def __init__(self) -> None:
        """Initialize an empty PriorityQueue.

        """
        self._items = []

    def __str__(self) -> str:
        """Return a string representation of the PriorityQueue"""
        output = "EVENT LIST"
        for x in self._items:
            output += " | " + str(x)
        return output

    def remove(self) -> object:
        """Remove and return the next item from this PriorityQueue.

        Precondition: <self> should not be empty.

        >>> pq = PriorityQueue()
        >>> pq.add("red")
        >>> pq.add("blue")
        >>> pq.add("yellow")
        >>> pq.add("green")
        >>> pq.remove()
        'blue'
        >>> pq.remove()
        'green'
        >>> pq.remove()
        'red'
        >>> pq.remove()
        'yellow'
        """
        return self._items.pop(0)

    def is_empty(self) -> bool:
        """
        Return true iff this PriorityQueue is empty.

        >>> pq = PriorityQueue()
        >>> pq.is_empty()
        True
        >>> pq.add("thing")
        >>> pq.is_empty()
        False
        """
        return len(self._items) == 0

    def add(self, item: object) -> None:
        """Add <item> to this PriorityQueue.

        >>> pq = PriorityQueue()
        >>> pq.add("yellow")
        >>> pq.add("blue")
        >>> pq.add("red")
        >>> pq.add("green")
        >>> pq._items
        ['blue', 'green', 'red', 'yellow']
        """
        inserted = False  # check within the for loop if item has been inserted
        new_items = []  # initialize the new list which will replace self._items
        for i in range(len(self._items)):
            # iterate over self._items and check if item < current item
            if not inserted and item < self._items[i]:
                # if item is smaller than the current item, insert it into the
                # list, and note that the item has been inserted
                new_items.append(item)
                inserted = True
            new_items.append(self._items[i])  # add the next item
        if not inserted:
            # this case happens when item is greater than all the items in
            # self._items, leaving item to be at the end of the updated list
            new_items.append(item)
        # replace self._items with new_items
        self._items = new_items


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
