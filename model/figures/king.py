from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Color
from .figure import Figure

if TYPE_CHECKING:
    from ..board import Board

class King(Figure):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)

    def clone_fig(self) -> King:
        clon: King = King(self.get_x(), self.get_y(), self.get_color())
        clon._count_movements = self.get_move_count()
        return clon

    def king_moves(self, board: Board, dx: int, dy: int) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []
        x = self.get_x() + dx
        y = self.get_y() + dy
        if self.out_of_bounds(x, y):
            return moves
        fig = board.get_figure_at(x, y)
        if fig is not None:
            if fig.is_enemy(self):
                moves.append((x, y))
            return moves
        moves.append((x, y))
        return moves
    
    def available_positions(self, board: Board) -> list[tuple[int, int]]:
        r = self.king_moves(board, 1, 0)
        l = self.king_moves(board, -1, 0)
        u = self.king_moves(board, 0, 1)
        d = self.king_moves(board, 0, -1)
        ur = self.king_moves(board, 1, 1)
        ul = self.king_moves(board, -1, 1)
        dr = self.king_moves(board, 1, -1)
        dl = self.king_moves(board, -1, -1)
        return r + l + u + d + ur + ul + dr + dl
