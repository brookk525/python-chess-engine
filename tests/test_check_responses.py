from model.match import Match
from model.enums import Color
from model.king import King
from model.rook import Rook
from model.bishop import Bishop


def _clear_board(board):
    for fig in list(board.get_figures()):
        board._remove_figure(fig)


def test_in_check_king_can_move_to_safe_square():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    _clear_board(board)

    white_king = King(4, 0, Color.WHITE)
    black_rook = Rook(4, 7, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_rook)

    # Está en jaque al inicio
    assert m.is_in_check(Color.WHITE, board) is True
    assert m.get_turn() == Color.WHITE

    # Mover el rey a una casilla segura (sale de la columna atacada)
    ok = m.move(white_king, 3, 0)

    assert ok is True
    assert (white_king.get_x(), white_king.get_y()) == (3, 0)
    assert board.get_figure_at(3, 0) is white_king
    assert m.is_in_check(Color.WHITE, board) is False


def test_in_check_can_capture_attacking_piece_to_resolve_check():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    _clear_board(board)

    white_king = King(4, 0, Color.WHITE)
    black_rook = Rook(4, 7, Color.BLACK)

    # Alfil blanco que puede capturar la torre negra en diagonal
    white_bishop = Bishop(1, 4, Color.WHITE)

    board._add_figure(white_king)
    board._add_figure(black_rook)
    board._add_figure(white_bishop)

    # El rey blanco está en jaque
    assert m.is_in_check(Color.WHITE, board) is True
    assert m.get_turn() == Color.WHITE

    # Captura la pieza que da jaque
    ok = m.move(white_bishop, 4, 7)

    assert ok is True
    assert board.get_figure_at(4, 7) is white_bishop
    assert black_rook not in board.get_figures()
    assert m.is_in_check(Color.WHITE, board) is False
