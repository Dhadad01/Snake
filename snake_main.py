from typing import Optional

import game_parameters
from game_display import GameDisplay

from game import Game
from snake import Direction
from board import Board

KEY_TO_DIRECTION = {
    "Up": Direction.UP,
    "Down": Direction.DOWN,
    "Right": Direction.RIGHT,
    "Left": Direction.LEFT,
}


def draw(board: Board, gd: GameDisplay, score: int) -> None:
    """
    draw all the board cells & display the player score.

    :param board: the board to draw.
    :param gd: drawing & display object.
    :param score: the score of the player
    """
    board.update()
    for cell, color in board.get_cells().items():
        column, row = cell
        gd.draw_cell(column, row, color)

    gd.show_score(score)


def get_direction_from_user(gd: GameDisplay) -> Optional[Direction]:
    """
    translate the key clicked by the user to a direction value acceptable by
    the game.
    """
    key_clicked = gd.get_key_clicked()

    if key_clicked is None:
        return None

    return KEY_TO_DIRECTION.get(key_clicked)


def setup_game(gd: GameDisplay) -> Game:
    """
    setup the game, initialize all the required object & elements of the game.

    :param gd: drawing & display object.
    """
    game = Game(game_parameters.WIDTH, game_parameters.HEIGHT)
    game.create_snake()
    game.create_bomb()
    for _ in range(Game.AMOUNT_OF_APPLES):
        game.create_apple()

    return game


def main_loop(gd: GameDisplay) -> None:
    game = setup_game(gd)
    while game.is_playing():
        draw(game.get_board(), gd, game.get_score())
        gd.end_round()
        direction = get_direction_from_user(gd)
        game.single_turn(direction)
    draw(game.get_board(), gd, game.get_score())
    gd.end_round()

