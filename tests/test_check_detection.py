from model.match import Match
from model.enums import Color
from model.king import King
from model.rook import Rook
from model.pawn import Pawn


def test_is_in_check_true_when_rook_attacks_king_on_open_file():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    board.clear()

    white_king = King(4, 0, Color.WHITE)
    black_rook = Rook(4, 7, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_rook)

    assert m.is_in_check(Color.WHITE, board) is True


def test_is_in_check_false_when_line_is_blocked():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    board.clear()

    white_king = King(4, 0, Color.WHITE)
    black_rook = Rook(4, 7, Color.BLACK)

    # Pieza blanca bloqueando la columna
    blocker = Pawn(4, 3, Color.WHITE)

    board._add_figure(white_king)
    board._add_figure(black_rook)
    board._add_figure(blocker)

    assert m.is_in_check(Color.WHITE, board) is False
