from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums import Color
from .figure import Figure

if TYPE_CHECKING:
    from ..board import Board

class Pawn(Figure):
    def __init__(self, x: int, y: int, color: Color):
        super().__init__(x, y, color)

    def clone_fig(self) -> Pawn:
        clon: Pawn = Pawn(self.get_x(), self.get_y(), self.get_color())
        clon._count_movements = self.get_move_count()
        return clon

    def available_positions(self, board: Board) -> list[tuple[int, int]]:
        
        moves: list[tuple[int, int]] = []
        direction_y = 1 if self.get_color() == Color.WHITE else -1

        x = self.get_x()
        y = self.get_y() + direction_y
        if self.out_of_bounds(x, y):
            return moves
            
        if self.can_capture(board, x -1, y):
            moves.append((x - 1, y))

        if self.can_capture(board, x +1, y):
            moves.append((x + 1, y))

        fig = board.get_figure_at(x, y)
        if fig is not None:
                return moves
        
        moves.append((x, y))
        #Doble paso
        if self.get_move_count() == 0:
            y = self.get_y() + direction_y * 2
            if self.out_of_bounds(x, y):
                return moves
            fig2 = board.get_figure_at(x, y)
            if fig2 is not None:
                    return moves
            moves.append((x, y))
        return moves

    def can_capture(self, board: Board, x: int, y: int) -> bool:
        if not self.out_of_bounds(x, y):
            fig_target = board.get_figure_at(x, y)
            if fig_target is not None:
                if fig_target.is_enemy(self):
                    return True
        return False
