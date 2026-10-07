from __future__ import annotations

from typing import TYPE_CHECKING

from .enums import Color
from .figure import Figure

if TYPE_CHECKING:
    from .board import Board

class Bishop(Figure):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)

    def clone_fig(self) -> Bishop:
        clon: Bishop = Bishop(self.get_x(), self.get_y(), self.get_color())
        clon._count_movements = self.get_move_count()
        return clon

    def available_positions(self, board: Board) -> list[tuple[int, int]]:
        ur = self._atr_moves(board, 1, 1)
        ul = self._atr_moves(board, -1, 1)
        dr = self._atr_moves(board, 1, -1)
        dl = self._atr_moves(board, -1, -1)
        return ur + ul + dr + dl