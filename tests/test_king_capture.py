from model.enums import Color
from model.figures.king import King
from model.match import Match
from model.figures.rook import Rook


def test_move_cannot_capture_enemy_king():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    board.clear()

    white_king = King(7, 0, Color.WHITE)
    black_king = King(0, 7, Color.BLACK)
    white_rook = Rook(0, 6, Color.WHITE)

    board._add_figure(white_king)
    board._add_figure(black_king)
    board._add_figure(white_rook)

    turn_before = m.get_turn()

    ok = m.move(white_rook, 0, 7)

    assert ok is False
    assert board.get_figure_at(0, 7) is black_king
    assert board.get_figure_at(0, 6) is white_rook
    assert m.get_turn() == turn_before
