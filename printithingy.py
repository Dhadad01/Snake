from enum import Enum
from typing import *


class Direction(Enum):
    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"


class Snake:
    def __init__(self, location: Tuple[int, int]) -> None:
        self.head = location
        self.coordinates = [(self.head[0], self.head[1] - 2), (self.head[0], self.head[1] - 1), self.head]
        self.color = "Black"
        self.direction = Direction.UP

    def get_color(self) -> AnyStr:
        return self.color

    def get_coordinates(self) -> List(Tuple[int, int]):
        return self.coordinates

    def move(self) -> None:
        self.coordinates.pop(0)
        if self.direction is Direction.UP:
            self.coordinates.append((self.head[0], self.head[1] + 1))
        elif self.direction is Direction.DOWN:
            self.coordinates.append((self.head[0], self.head[1] - 1))
        elif self.direction is Direction.RIGHT:
            self.coordinates.append((self.head[0] + 1, self.head[1]))
        elif self.direction is Direction.LEFT:
            self.coordinates.append((self.head[0] - 1, self.head[1]))
        self.head = self.coordinates[-1]

    def get_head(self):
        return self.head

    def valid_move(self, move: Direction) -> bool:
        all_moves = [[Direction.DOWN, Direction.UP], [Direction.RIGHT, Direction.LEFT]]
        if self.direction is not move:
            if (self.direction in all_moves[0] and move in all_moves[1]) or \
                    (self.direction in all_moves[1] and move in all_moves[0]):
                return True
            return False  # thats the opposite direction - not a valid move
        return True  # same direction is valid

    def change_direction(self, move: Direction) -> bool:
        if not self.valid_move(move):
            return False
        self.direction = move
        return True

    def eat_apple(self) -> None:
        if self.direction is Direction.UP:
            self.coordinates.extend([(self.head[0], self.head[1] + 1), (self.head[0], self.head[1] + 2),
                                     (self.head[0], self.head[1] + 3)])
        elif self.direction is Direction.DOWN:
            self.coordinates.extend([(self.head[0], self.head[1] - 1), (self.head[0], self.head[1] - 2),
                                     (self.head[0], self.head[1] - 3)])
        elif self.direction is Direction.RIGHT:
            self.coordinates.extend([(self.head[0] + 1, self.head[1]), (self.head[0] + 2, self.head[1]),
                                     (self.head[0] + 3, self.head[1])])
        elif self.direction is Direction.LEFT:
            self.coordinates.extend([(self.head[0] - 1, self.head[1]), (self.head[0] - 2, self.head[1]),
                                     (self.head[0] - 3, self.head[1])])
        self.head = self.coordinates[-1]


class Apple:
    def __init__(self, location, score) -> None:
        self.coordinates = location
        self.color = "Green"
        self.score = score

    def get_color(self) -> AnyStr:
        return self.color

    def get_coordinates(self) -> Tuple:
        return self.coordinates

    def get_score(self):
        return self.score
