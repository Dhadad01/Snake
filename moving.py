from printable_object import PrintableObject


class Moving(PrintableObject):
    """
    API for all printable object which can move.
    """

    def move(self) -> None:
        """
        start a single moving action of the object.
        """
        raise NotImplementedError()
