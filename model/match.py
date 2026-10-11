from __future__ import annotations

from .enums import Color, Side, MatchState, PromotingType
from .board import Board
from .mutable_board import MutableBoard
from .figure import Figure

from .pawn import Pawn
from .rook import Rook
from .knight import Knight
from .bishop import Bishop
from .queen import Queen
from .king import King

class Match:
    def __init__(self, match_id: int, player1_name: str, player2_name: str):
        self.__id: int = match_id
        self._board: MutableBoard = MutableBoard()
        self._player1_name: str = player1_name
        self._player2_name: str = player2_name
        self._turn: Color = Color.WHITE
        self._state: MatchState = MatchState.WAITING
        self._pawn_to_promote: Pawn | None = None # Necesario para Promocionar
        


    def get_id(self) -> int:
        return self.__id

    def get_turn(self) -> Color:
        return self._turn

    def get_match_state(self) -> MatchState:
        return self._state

    def setup_pawns(self, color: Color):
        # 8 peones
        if color == Color.WHITE:
            fila = 1
        else:
            fila = 6
        for i in range(8):
            self._board._add_figure(Pawn(i, fila, color))
    
    def setup_back_row(self, color: Color):
        # 2 torres, 2 caballos, 2 alfiles, 1 reina y 1 rey.
        if color == Color.WHITE:
            fila = 0
        else:
            fila = 7
        for i in range(8):
            if i == 0 or i == 7:
                #2 torres
                self._board._add_figure(Rook(i, fila, color))
            elif i == 1 or i == 6:
                #2 caballos
                self._board._add_figure(Knight(i, fila, color))
            elif i == 2 or i == 5:
                #2 alfiles
                self._board._add_figure(Bishop(i, fila, color))
            elif i == 3:
                #1 reina
                self._board._add_figure(Queen(i, fila, color))
            else:
                #1 rey
                self._board._add_figure(King(i, fila, color))
        

    def generate_team(self, color: Color):
        self.setup_pawns(color)
        self.setup_back_row(color)

    def start(self):
        self._board.clear()
        self.generate_team(Color.WHITE)
        self.generate_team(Color.BLACK)
        self._turn = Color.WHITE
        self._state = MatchState.RUNNING

    def move(self, fig: Figure, x: int, y: int) -> bool:
        if fig is None or fig not in self._board.get_figures():
            return False   
        if self.get_match_state() == MatchState.RUNNING and fig.get_color() == self.get_turn():
            if isinstance(fig, King) and (x == 2 or x == 6) and fig.get_move_count() == 0:
                side = Side.LEFT if x == 2 else Side.RIGHT
                if self.can_castle(fig.get_color(), side):
                    self.castle(fig.get_color(), side)
                    return True
                else: return False
            if fig.can_move(x, y, self._board):
                target = self._board.get_figure_at(x, y)
                if isinstance(target, King):
                    return False

                ghost = self._board._clone_board()
                ghost_fig = ghost.get_figure_at(fig.get_x(), fig.get_y())
                ghost.move(ghost_fig, x, y)
                if self.is_in_check(fig.get_color(), ghost):
                    return False
                self._board.move(fig, x, y)
                fig.update_count_movements()
                color = fig.get_color()
                if self.is_promoting(color):
                    pawn = self.get_promoting_pawn(color)
                    if pawn is not None:
                        self._pawn_to_promote = pawn
                        self._state = MatchState.WAITING_PROMOTION
                    return True
                self._change_turn()
                return True
        return False

    def _change_turn(self):
        if self.get_turn() == Color.WHITE:
            self._turn = Color.BLACK
        else:
            self._turn = Color.WHITE

                                    # Este board será un self._board.clone()
    def is_in_check(self, color: Color, board: Board) -> bool:
        #comprobar si en los posibles movimientos de una figura, se encuentra el rey
        # ir comprobando pares de (X, Y) de la tupla de available positions de una figura:
        for figura in board.get_figures():
            if figura.get_color() != color:
                fig = figura
                for tupla in fig.available_positions(board):
                    x, y = tupla # Asi se desempaqueta una tupla
                    figure = board.get_figure_at(x, y) 
                    if isinstance(figure, King) and figure.get_color() == color:
                        return True
        return False
    
    def is_in_check_and_mate(self, color: Color, board: MutableBoard) -> bool:
        if not self.is_in_check(color, board):
            return False
        for fig in board.get_figures():
            if fig.get_color() != color:
                continue
            for tupla in fig.available_positions(board):
                x, y = tupla
                ghost = board._clone_board() # Si clono el tablero en cada iteracion, al terminar la vuelta, el rollback es automatico, y ya no hay margen de error
                fig_ghost = ghost.get_figure_at(fig.get_x(), fig.get_y())
                ghost.move(fig_ghost, x, y)
                if not self.is_in_check(color, ghost):  # si dejo de estar en jaque simulando este movimiento, significa q puedo salvarme y no estoy en jaque mate
                    return False
        return True

    def can_castle(self, color: Color, side: Side) -> bool:
        if not self.is_in_check(color, self._board):
            rky = 0 if color == Color.WHITE else 7
            
            left_rook = self._board.get_figure_at(0, rky)
            king = self._board.get_figure_at(4, rky)
            right_rook = self._board.get_figure_at(7, rky)

            if side == Side.LEFT:
                if isinstance(left_rook, Rook) and isinstance(king, King) and not left_rook.is_enemy(king):
                    if left_rook.get_move_count() == 0 and king.get_move_count() == 0:
                        for i in range(1, 4):
                            x = king.get_x() - i 
                            fig = self._board.get_figure_at(x, rky)
                            if fig is not None:
                                return False
                            ghost = self._board._clone_board()
                            ghost_king = ghost.get_figure_at(king.get_x(), king.get_y())
                            ghost.move(ghost_king, x, ghost_king.get_y())
                            if self.is_in_check(ghost_king.get_color(), ghost):
                                return False
                        return True
                
            if side == Side.RIGHT:
                if isinstance(right_rook, Rook) and isinstance(king, King) and not right_rook.is_enemy(king):
                    if right_rook.get_move_count() == 0 and king.get_move_count() == 0:
                        for i in range(1, 3):
                            x = king.get_x() + i 
                            fig = self._board.get_figure_at(x, rky)
                            if fig is not None:
                                return False
                            ghost = self._board._clone_board()
                            ghost_king = ghost.get_figure_at(king.get_x(), king.get_y())
                            ghost.move(ghost_king, x, ghost_king.get_y())
                            if self.is_in_check(ghost_king.get_color(), ghost):
                                return False
                        return True
                
            return False

    def castle(self, color: Color, side: Side ):
        rky = 0 if color == Color.WHITE else 7
        left_rook = self._board.get_figure_at(0, rky)
        king = self._board.get_figure_at(4, rky)
        right_rook = self._board.get_figure_at(7, rky)
        if side == Side.LEFT:
            x_aux = left_rook.get_x()
            y_aux = left_rook.get_y()
            x_king = king.get_x()
            y_king = king.get_y()

            left_rook.set_x(x_king -1)
            left_rook.set_y(y_king)
            king.set_x(x_aux + 2)
            king.set_y(y_aux)
            left_rook.update_count_movements()

        if side == Side.RIGHT:
            x_aux = right_rook.get_x()
            y_aux = right_rook.get_y()
            x_king = king.get_x()
            y_king = king.get_y()

            right_rook.set_x(x_king + 1)
            right_rook.set_y(y_king)
            king.set_x(x_aux - 1)
            king.set_y(y_aux)
            right_rook.update_count_movements()
        king.update_count_movements()
        self._change_turn()

    def is_stalemate(self, color: Color, board: MutableBoard) -> bool:
        if not self.is_in_check(color, board) and self.get_turn() == color:
            for fig in board.get_figures():
                if fig.get_color() != color:
                    continue
                for tupla in fig.available_positions(board):
                    x, y = tupla
                    ghost = board._clone_board()
                    ghost_fig = ghost.get_figure_at(fig.get_x(), fig.get_y())
                    ghost.move(ghost_fig, x, y)
                    if not self.is_in_check(color, ghost): # si dejo de estar en jaque simulando este movimiento, significa q puedo salvarme y no estoy ahogado
                        return False
            return True
        return False        

    def is_promoting(self, color: Color) -> bool:
        return self.get_promoting_pawn(color) is not None

    def get_promoting_pawn(self, color: Color) -> Pawn | None:
        y_promote = 0 if color == Color.BLACK else 7
        for i in range(8):
            fig = self._board.get_figure_at(i, y_promote)
            if fig is not None and fig.get_color() == color and isinstance(fig, Pawn):
                    return fig
        return None  

    def promote(self, desired_type: PromotingType):
        if self._pawn_to_promote is None or not isinstance(desired_type, PromotingType):
            return

        promoting_pawn = self._pawn_to_promote
        color = promoting_pawn.get_color()
        x = promoting_pawn.get_x()
        y = promoting_pawn.get_y()

        self._board._remove_figure(promoting_pawn)
        if desired_type == PromotingType.QUEEN:
            self._board._add_figure(Queen(x, y, color))

        elif desired_type == PromotingType.KNIGHT:
            self._board._add_figure(Knight(x, y, color))

        elif desired_type == PromotingType.BISHOP:
            self._board._add_figure(Bishop(x, y, color))
        
        elif desired_type == PromotingType.ROOK:
            self._board._add_figure(Rook(x, y, color))
        
        self._pawn_to_promote = None
        self._state = MatchState.RUNNING
        self._change_turn()
