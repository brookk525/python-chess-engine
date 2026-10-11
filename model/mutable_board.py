from __future__ import annotations

from typing import TYPE_CHECKING

from .board import Board

if TYPE_CHECKING:
    from .figures.figure import Figure

class MutableBoard(Board):
    def __init__(self):
        super().__init__()

    def move(self, fig: Figure, x: int, y: int):
        self._set_figure_at(fig, x, y)  

    def _set_figure_at(self, fig: Figure, x: int, y: int):
        f = self.get_figure_at(x, y)
        if f is not None:
            self._remove_figure(f)
        fig.set_x(x)
        fig.set_y(y)

    def _clone_board(self) -> MutableBoard:
            clon: MutableBoard = MutableBoard()
            for fig in self.get_figures():
                fig_clon = fig.clone_fig()
                clon._add_figure(fig_clon)
            return clon
    
    def _add_figure(self, fig: Figure):
        self._figures.append(fig)

    def _remove_figure(self, fig: Figure):
        self._figures.remove(fig)

    def clear(self):
        self._figures = []
