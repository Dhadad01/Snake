from enum import Enum
from typing import List, Tuple

from moving import Moving


class Direction(Enum):
    """
    enum of directions.
    """
    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"


class Snake(Moving):
    """
    a class representing a snake in the game.
    """
    APPLE_WAS_EATEN_GROWTH = 3
    COLOR = "black"

    def __init__(self, location: Tuple[int, int]) -> None:
        """
        create a new snake.

        :param location: where to initially locate the head of the snake.
        """

        self._head = location
        self._coordinates = [
            (self._head[0], self._head[1] - 2),
            (self._head[0], self._head[1] - 1),
            self._head
        ]
        self._direction = Direction.UP
        self._growth_counter = 0

    def get_color(self) -> str:
        """
        return the color of the snake.
        """
        return self.COLOR

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        return a list of cells coordinates occupied by the snake body.
        """
        return self._coordinates

    def move(self) -> None:
        """
        move the snake.
        """
        if self._growth_counter == 0:
            self._coordinates.pop(0)
        else:
            self._growth_counter -= 1

        if self._direction is Direction.UP:
            self._coordinates.append((self._head[0], self._head[1] + 1))
        elif self._direction is Direction.DOWN:
            self._coordinates.append((self._head[0], self._head[1] - 1))
        elif self._direction is Direction.RIGHT:
            self._coordinates.append((self._head[0] + 1, self._head[1]))
        elif self._direction is Direction.LEFT:
            self._coordinates.append((self._head[0] - 1, self._head[1]))
        self._head = self._coordinates[-1]

    def get_head(self) -> Tuple[int, int]:
        """
        return the coordinates of the cell occupied by the snake's head.
        """
        return self._head

    def _valid_move(self, move: Direction) -> bool:
        all_moves = [[Direction.DOWN, Direction.UP],
                     [Direction.RIGHT, Direction.LEFT]]
        if self._direction is not move:
            if (self._direction in all_moves[0] and move in all_moves[1]) or \
                    (self._direction in all_moves[1] and move in all_moves[0]):
                return True
            # thats the opposite direction - not a valid move
            return False
        # same direction is valid
        return True

    def change_direction(self, move: Direction) -> bool:
        """
        :param move: in which direction the snake should be moving.
        :return: whether or not the direction of the snake was successfully
                 altered.
        """
        if not self._valid_move(move):
            return False
        self._direction = move
        return True

    def eat_apple(self) -> None:
        """
        "eat an apple" & increment the snake's body length.
        """
        self._growth_counter += self.APPLE_WAS_EATEN_GROWTH
