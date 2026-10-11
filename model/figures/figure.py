from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ..enums import Color

if TYPE_CHECKING:
    from ..board import Board

class Figure(ABC):
    def __init__(self, x: int, y: int, color: Color):
        self._x: int = x
        self._y: int = y
        self._color: Color = color
        self._count_movements: int = 0

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y
    
    def set_x(self, x: int):
        if x < 0:
            raise ValueError("La x ha de ser mayor o igual a 0")
        if x > 7:
            raise ValueError("La x ha de ser menor o igual a 7")
        self._x = x
                                    #Esto es necesario, para poder acceder a su X y su Y desde otra clase
    def set_y(self, y: int):
        if y < 0:
            raise ValueError("La y ha de ser mayor o igual a 0")
        if y > 7:
            raise ValueError("La y ha de ser menor o igual a 7")
        self._y = y

    @abstractmethod
    def clone_fig(self) -> Figure:  # Necesito esta funcion para poder hacer Simulaciones de movimientos, y no usar el tablero real por si acaso
        pass

    def update_count_movements(self):
        self._count_movements += 1

    def get_move_count(self):
        return self._count_movements

    def get_color(self) -> Color:
        return self._color

    # Función necesaria para saber donde se pueden mover las Figuras desde la posicion en la que están
    @abstractmethod
    def available_positions(self, board: Board) -> list[tuple[int, int]]:
        pass

    def can_move(self, x: int, y: int, board: Board) -> bool:
        return (x, y) in self.available_positions(board)
    
    def out_of_bounds(self, x: int, y: int) -> bool:
        return x < 0 or x > 7 or y < 0 or y > 7

    def is_enemy(self, other: Figure) -> bool:
        return self.get_color() != other.get_color()
    
    def _atr_moves(self, board: Board, dx: int, dy: int) -> list[tuple[int, int]]:
        moves: list[tuple[int, int]] = []
        for i in range(1, 8):
            x = self.get_x() + i * dx
            y = self.get_y() + i * dy
            if self.out_of_bounds(x, y):
                break

            fig = board.get_figure_at(x, y)
            if fig is not None:
                if fig.is_enemy(self):
                    moves.append((x, y))
                break
                    
            moves.append((x, y))
        return moves
    
