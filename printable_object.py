from typing import List, Tuple


class PrintableObject:
    def get_coordinates(self) -> List[Tuple[int, int]]:
        raise NotImplemented()

    def __eq__(self, other) -> bool:
        return (self.get_color() == other.get_color() and
                self.get_coordinates() == other.get_coordinates())

    def get_color(self) -> str:
        raise NotImplemented()
