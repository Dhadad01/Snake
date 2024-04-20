from typing import Tuple, List, Set
from moving import Moving


class Bomb(Moving):
    """
    a class representing a single bomb in the game.
    """
    MININAL_RADIUS = 1
    EXPLOSION_THRESHOLD = 1
    COLOR_BEFORE_DETONATION = "red"
    COLOR_AFTER_DETONATION = "orange"

    def __init__(self,
                 location: Tuple[int, int],
                 radius: int,
                 turns_until_explosion: int) -> None:
        """
        create a new bomb.

        :param location: the bomb coordinates.
        :param radius: the bomb explosion radius.
        :param turns_until_explosion: how many turns, i.e. calls to "move",
                                      before the bomb detonation.
        """
        if self._radius_invalid(radius):
            raise ValueError(f"radius {radius} must be greater than 0")
        if self._invalid_turns_until_explosion(turns_until_explosion):
            raise ValueError("turns until explosion must be greater than 0")

        self._detonated = False
        self._max_radius = radius
        self._radius = 0
        self._turns_until_explosion = turns_until_explosion
        self._location = location

    def _radius_invalid(self, radius: int) -> bool:
        return radius < self.MININAL_RADIUS

    def _invalid_turns_until_explosion(self, turns: int) -> bool:
        return turns <= self.EXPLOSION_THRESHOLD

    def get_color(self) -> str:
        """
        return the color of the bomb.
        red before detonation & orange after detonation.
        """
        if not self._detonated:
            return self.COLOR_BEFORE_DETONATION
        else:
            return self.COLOR_AFTER_DETONATION

    def move(self) -> None:
        """
        "move" the bomb, i.e. count-down until explosion if the bomb haven't
        already detonated or advance the explosion shock-wave ripples.
        """
        if self._turns_until_explosion > self.EXPLOSION_THRESHOLD:
            self._turns_until_explosion = self._turns_until_explosion - 1
            return

        # just exploded.
        if self._detonated is False:
            self._detonated = True
            self._radius = 0
            return

        # already exploded
        else:
            # advance the shock-wave
            self._radius = self._radius + 1

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        return the coordinates of cells occupied either by the bomb itself
        before detonation or cell occupied by the explosion shock-wave ripples.

        :return: list of cells coordinates occupied by the bomb.
        """

        if self._detonated:
            return self.shockwave_ripples(self._radius)
        else:
            return self.shockwave_ripples(0)

    def shockwave_ripples(self, radius: int) -> List[Tuple[int, int]]:
        """
        evaluate the advance of the shock-wave based on the bomb original
        position & current explosion radius.

        :param radius: current explosion radius.
        :return: list of coordinates of cells currently occupied by the
                 shock-wave ripples.
        """
        points = set()  # type: Set[Tuple[int, int]]
        x, y = self._location

        for i in range(0, radius + 1, 1):  # [0, radius]
            for k in range(0, i + 1, 1):  # [0 , i]
                points.add((x + k, y + (radius - k)))
                points.add((x + k, y - (radius - k)))
                points.add((x - k, y + (radius - k)))
                points.add((x - k, y - (radius - k)))

        return list(points)

    def attack_is_over(self) -> bool:
        """
        check whether or not the bomb detonated & the shock-wave have faded.
        """
        return self._radius > self._max_radius
