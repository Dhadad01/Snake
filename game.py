from typing import List, Optional
from collections import Counter

import game_parameters

from snake import Snake, Direction
from apple import Apple
from board import Board
from bomb import Bomb


class Game:
    """
    a class which is responsible for enforcing the rules of the game.
    """

    AMOUNT_OF_APPLES = 3
    COLOR_STRENGTHS = {
        "green": 0,  # apple.
        "black": 1,  # snake.
        "red": 2,  # un-detonated bomb.
        "orange": 3,  # detonated bomb.
    }

    def __init__(self, length: int, height: int):
        """
        create a new game.

        :param length: the length of the board of the new game.
        :param height: the height of the board of the new game.
        """
        self._board = Board(length, height, Game.COLOR_STRENGTHS)
        self._playing = True
        self._score = 0
        self._bombs = []  # type: List[Bomb]
        self._apples = []  # type: List[Apple]

    def get_score(self) -> int:
        """
        return the player score.
        """
        return self._score

    def create_snake(self) -> None:
        """
        create a new snake object.
        """
        x = self._board.get_length() // 2
        y = self._board.get_height() // 2
        self._snake = Snake((x, y))
        self._board.add_element(self._snake)

    def create_apple(self) -> None:
        """
        create a new apple object.
        """
        if self._board.is_full():
            self._playing = False
            return

        added = False
        while not added:
            x, y, score = game_parameters.get_random_apple_data()
            apple = Apple((x, y), score)
            added = self._board.add_element(apple)

        self._apples.append(apple)

    def create_bomb(self) -> None:
        """
        create a new bomb object.
        """
        added = False
        while not added:
            x, y, radius, time_to_explode = \
                game_parameters.get_random_bomb_data()
            bomb = Bomb((x, y), radius, time_to_explode)
            added = self._board.add_element(bomb)

        self._bombs.append(bomb)

    def single_turn(self, direction: Optional[Direction]) -> None:
        """
        execute a single turn.
        in each turn the following actions occurs (in the following order):
        1) the snake might change direction, based on the given direction.
        2) the snake executes a single move action.
        3) verification that the snake is still alive.
        4) checking if the snake ate an apple (and acting accordingly).
        5) "detonating" all the bomb, i.e. decreasing their detonation counter
           if the haven't exploded yet, or advancing the shock-wave ripples.
        6) checking once more if the snake have died (by the
           shock-wave ripples).
        7) replacing exploded apples & faded-out bombs.

        :param direction: in which direction the snake should move.
        """
        if direction is not None:
            self._snake.change_direction(direction)
        self._snake.move()

        if self._did_snake_died():
            self._playing = False
            return

        self._snake_ate_apple()

        self._detonate_bombs()

    def _did_snake_died(self) -> bool:
        """
        check if the snake have died.

        there are numerous reasons for the snake to die:
        1) the snake have crash into himself.
        2) the snake have crash into a wall.
        3) the snake have exploded by a bomb.

        :return: whether or not the snake have died.
        """
        # check if snake crash into himself.
        counter = Counter(self._snake.get_coordinates())
        _, occurences = counter.most_common(1)[0]

        if occurences > 1:
            return True

        # check if snake crash into a wall.
        for cell in self._snake.get_coordinates():
            if not self._board.is_cell_in_board(cell):
                return True

        # check if snake went kaboom.
        snake_cells = set(self._snake.get_coordinates())
        for bomb in self._bombs:
            bomb_cells = set(bomb.get_coordinates())
            if snake_cells.intersection(bomb_cells):
                return True

        return False

    def _snake_ate_apple(self) -> None:
        """
        check if the snake ate an apple & act accordingly.
        """
        found_apple = None

        head = set([self._snake.get_head()])
        for apple in self._apples:
            apple_cells = set(apple.get_coordinates())
            if head.intersection(apple_cells):
                found_apple = apple
                break

        if found_apple:
            # increment the player score.
            self._score += found_apple.get_score()
            # increment the snake's length.
            self._snake.eat_apple()
            # create a new apple instead of the eaten one.
            self._replace_apples([found_apple])

    def _replace_apples(self, apples_to_replace: List[Apple]) -> None:
        """
        remove apples from the game & board.
        add, the same amount of removed apples, new apples into the game.

        :param apples_to_replace: list of eaten apples to replace with
                                  new bombs.
        """
        for apple in apples_to_replace:
            self._apples.remove(apple)
            self._board.remove_element(apple)
            self.create_apple()

    def _replace_bombs(self, bombs_to_replace: List[Bomb]) -> None:
        """
        remove bombs from the game & board.
        add, the same amount of removed bombs, new bombs into the game.

        :param bombs_to_remove: list of exploded bombs (which already faded
                                away) to replace with new bombs.
        """
        for bomb in bombs_to_replace:
            self._bombs.remove(bomb)
            self._board.remove_element(bomb)
            self.create_bomb()

    def _detonate_bombs(self) -> None:
        """
        "detonate" each & every bomb.
        """
        bombs_to_remove = []  # type: List[Bomb]
        apples_to_remove = []  # type: List[Apple]

        for bomb in self._bombs:
            bomb.move()
            apples_to_remove = self._find_exploded_apples(bomb)
            if bomb.attack_is_over():
                bombs_to_remove.append(bomb)

        if self._did_snake_died():
            self._playing = False
            return

        self._replace_bombs(bombs_to_remove)

        self._replace_apples(apples_to_remove)

    def _find_exploded_apples(self, bomb: Bomb) -> List[Apple]:
        """
        find all apples which have exploded by a specific bomb.

        :param bomb: a bomb.
        :return: list of all apples exploded by the given bomb.
        """
        apples_to_remove = []  # type: List[Apple]

        for apple in self._apples:
            apple_cells = set(apple.get_coordinates())
            if apple_cells.intersection(set(bomb.get_coordinates())):
                apples_to_remove.append(apple)

        return apples_to_remove

    def get_board(self) -> Board:
        """
        return the game's board.
        """
        return self._board

    def is_playing(self) -> bool:
        """
        check if the game is still playing.
        """
        return self._playing
