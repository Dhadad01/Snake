from typing import List, Tuple, Optional, Dict, cast
from printable_object import PrintableObject


class Board:
    """
    A class which is responsible for evaluating how to display the board-game.
    """

    def __init__(self,
                 length: int,
                 height: int,
                 color_stengths: Dict[str, int]) -> None:
        """
        create a new board.

        :param length: desired length of the board.
        :param height: desired height of the board.
        :param color_stengths: a mapping between colors to their displaying
                               precedences.
        """
        if length <= 0:
            raise ValueError("length must be greater than zero")
        if height <= 0:
            raise ValueError("height must be greater than zero")
        self._elements = []  # type: List[PrintableObject]
        self._length = length
        self._height = height
        self._colors_stengths = color_stengths
        self._occupied_cells = {} # type: Dict[Tuple[int, int], str]

    def get_length(self) -> int:
        """
        return the length of the board.
        """
        return self._length

    def get_height(self) -> int:
        """
        return the height of the board.
        """
        return self._height

    def _empty_board(self) -> List[List[Optional[str]]]:
        """
        generate an empty board.
        """
        columns = []  # type: List[List[Optional[str]]]

        for i in range(self._length):
            column = []  # type: List[Optional[str]]
            for j in range(self._height):
                column.append(None)
            columns.append(column)

        return columns

    def board(self) -> List[List[Optional[str]]]:
        """
        evaluate the colors of each & every cell of the board.

        :return: matrix of the board cells content (represnting a color or
                 None if the cell is empty).
        """
        board = self._empty_board()

        for element in self._elements:
            for cell in element.get_coordinates():
                column, row = cell
                color = element.get_color()
                if not self.is_cell_in_board(cell):
                    continue
                # current cell isn't empty
                # use the "stronger" color.
                if board[column][row] is not None:
                    current_color = cast(str, board[column][row])
                    color = self.determine_color(current_color, color)
                board[column][row] = color

        return board

    def determine_color(self,
                        current_color: str,
                        color: str) -> str:
        """
        determine which color is "stronger", i.e. which color should be
        displayed.

        :param current_color: the color of a specific cell within board.
        :param color: a color candidate for the same cell within board.
        :return: color to display.
        """
        current_color_stength = self._color_stength(current_color)
        color_stength = self._color_stength(color)

        colors = {
            current_color_stength: current_color,
            color_stength: color,
        }

        return colors[max([current_color_stength, color_stength])]

    def cells_list(self) -> List[Tuple[int, int]]:
        """
        return a list of all the board cells coordinates.
        """
        cells = []  # type: List[Tuple[int, int]]

        for column in range(self._length):
            for row in range(self._height):
                cells.append((column, row))

        return cells

    def is_full(self) -> bool:
        """
        check if there are no empty cells in the board.
        """
        for cell in self.cells_list():
            if self.cell_is_empty(cell):
                return False
        return True

    def _color_stength(self, color: str) -> int:
        """
        :param color: a color name.
        :return: the precedence of that color.
        """
        always_overridden = min(self._colors_stengths.values())
        return self._colors_stengths.get(color, always_overridden - 1)

    def is_cell_in_board(self, cell: Tuple[int, int]) -> bool:
        """
        check if a given cell coordinates are within the board.
        """
        column, row = cell
        return row in range(self._height) and column in range(self._length)

    def get_cell(self, cell: Tuple[int, int]) -> Optional[str]:
        """
        retrieve a cell content pointed by the given coordinates.
        :param cell: coordinates of the requested cell.
        :return: cell's content.
        """
        """
        column, row = cell
        return self.board()[column][row]
        """
        return self._occupied_cells.get(cell)

    def cell_is_empty(self, cell: Tuple[int, int]) -> bool:
        """
        check if a the cell pointed by the given coordinates is empty.

        :param cell: coordinates of a cell.
        """
        return self.get_cell(cell) is None

    def add_element(self, element: PrintableObject) -> bool:
        """
        add a printable element/object to the board.

        :param element: an element to add to the board.
        :return: whether or not the adding action was successful.

        NOTE:
            reasons for failure:
            1) the given element was previously added to the board.
            2) at-least one of the cells occupied by the given element are
               out of the bounds of the board.
            3) at-least one of the cells occupied by the given element are
               already occupied by another element.
        """
        self.update()

        if element in self._elements:
            return False

        cells = element.get_coordinates()
        for cell in cells:
            if not self.is_cell_in_board(cell):
                return False

        for cell in cells:
            if not self.cell_is_empty(cell):
                return False

        self._elements.append(element)
        return True

    def remove_element(self, element: PrintableObject) -> None:
        """
        remove an element from the board.
        """
        if element in self._elements:
            self._elements.remove(element)

    def update(self) -> None:
        """
        re-evaluate the occupied cells.
        """
        self._occupied_cells.clear()
        b = self.board()

        for cell in self.cells_list():
            column, row = cell
            if b[column][row] is not None:
                self._occupied_cells[cell] = b[column][row]

    def get_cells(self) -> Dict[Tuple[int, int], Optional[str]]:
        """
        get a dict of all occupied cells coordinates & their
        respective colors.
        """
        # might do a copy hear so self._occupied_cells can't be affected
        # from outside.
        return self._occupied_cells