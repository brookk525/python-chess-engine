from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Color
from .figure import Figure

if TYPE_CHECKING:
    from ..board import Board

class Rook(Figure):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)
        
    def clone_fig(self) -> Rook:
        clon: Rook = Rook(self.get_x(), self.get_y(), self.get_color())
        clon._count_movements = self.get_move_count()
        return clon

    def available_positions(self, board: Board) -> list[tuple[int, int]]:
        r = self._atr_moves(board, 1, 0)
        l = self._atr_moves(board, -1, 0)
        u = self._atr_moves(board, 0, 1)
        d = self._atr_moves(board, 0, -1)
        return r + l + u + d
