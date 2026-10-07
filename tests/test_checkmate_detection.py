from model.match import Match
from model.enums import Color
from model.king import King
from model.rook import Rook
from model.queen import Queen
from model.bishop import Bishop


def _clear_board(board):
    for fig in list(board.get_figures()):
        board._remove_figure(fig)


def test_is_in_check_and_mate_true_for_simple_checkmate_position():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    _clear_board(board)

    # Blanco: rey arrinconado en h1 (7,0)
    white_king = King(7, 0, Color.WHITE)

    # Negro: torre en h2 dando jaque + reina en g2 protegiendo la torre y controlando g1
    black_rook = Rook(7, 1, Color.BLACK)
    black_queen = Queen(6, 1, Color.BLACK)

    # Poner también el rey negro en una esquina (por si tu lógica lo necesita)
    black_king = King(0, 7, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_rook)
    board._add_figure(black_queen)
    board._add_figure(black_king)

    assert m.is_in_check(Color.WHITE, board) is True
    assert m.is_in_check_and_mate(Color.WHITE, board) is True


def test_is_in_check_and_mate_false_when_there_is_a_defense_available():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    _clear_board(board)

    # Igual que antes, pero en vez de reina usamos un alfil que solo protege la torre,
    # y así el rey blanco sí tiene la casilla g1 libre y segura.
    white_king = King(7, 0, Color.WHITE)

    black_rook = Rook(7, 1, Color.BLACK)
    black_bishop = Bishop(6, 2, Color.BLACK)  # g3 -> h2 diagonal, protege la torre
    black_king = King(0, 7, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_rook)
    board._add_figure(black_bishop)
    board._add_figure(black_king)

    assert m.is_in_check(Color.WHITE, board) is True
    assert m.is_in_check_and_mate(Color.WHITE, board) is False
