from __future__ import annotations

from typing import TYPE_CHECKING

from .enums import Color
from .figure import Figure

if TYPE_CHECKING:
    from .board import Board

class Knight(Figure):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)

    def clone_fig(self) -> Knight:
        clon: Knight = Knight(self.get_x(), self.get_y(), self.get_color())
        clon._count_movements = self.get_move_count()
        return clon

    def knight_moves(self, board: Board, dx: int, dy: int) -> list[tuple[int, int]]:
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
        ur = self.knight_moves(board, 1, 2)
        ul = self.knight_moves(board, -1, 2)
        dr = self.knight_moves(board, 1, -2)
        dl = self.knight_moves(board, -1, -2)
        ru = self.knight_moves(board, 2, 1)
        lu = self.knight_moves(board, -2, 1)
        rd = self.knight_moves(board, 2, -1)
        ld = self.knight_moves(board, -2, -1)

        return ur + ul + dr + dl + ru + lu + rd + ld
    