from typing import List, Tuple

from printable_object import PrintableObject


class Apple(PrintableObject):
    """
    a class representing an apple in the game.
    """
    COLOR = "green"

    def __init__(self, location: Tuple[int, int], score: int) -> None:
        """
        create a new apple.

        :param location: where to locate the apple.
        :param score: by which amount of points the player's score should
                      be incremented once the apple is eaten.
        """
        self.coordinate = location
        self.score = score

    def get_color(self) -> str:
        """
        return the color of the apple.
        """
        return self.COLOR

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        return a list of cells coordinates occupied by the apple.
        """
        return [self.coordinate]

    def get_score(self) -> int:
        """
        return the score added to the player once this apple is eaten.
        """
        return self.score
