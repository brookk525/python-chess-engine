from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .figure import Figure

class Board:
    def __init__(self):
        self._figures: list[Figure] = []

    def get_figure_at(self, x: int, y: int) -> Figure | None:
        for i in range(self.get_figure_count()):
            if self._figures[i].get_x() == x and self._figures[i].get_y() == y:
                return self._figures[i]
        return None

    def get_figure_count(self) -> int:
        return len(self._figures)
    
    def get_figures(self) -> list[Figure]:
        figures: list[Figure] = self._figures
        return figures.copy()

