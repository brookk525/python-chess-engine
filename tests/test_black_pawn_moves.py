from model.enums import Color
from model.match import Match


def _change_turn_to_black(match):
    board = match._board
    white_pawn = board.get_figure_at(7, 1)

    ok = match.move(white_pawn, 7, 2)

    assert ok is True
    assert match.get_turn() == Color.BLACK


def test_black_pawn_can_advance_one_if_free():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    _change_turn_to_black(m)
    pawn = board.get_figure_at(0, 6)

    ok = m.move(pawn, 0, 5)

    assert ok is True
    assert board.get_figure_at(0, 5) is pawn
    assert board.get_figure_at(0, 6) is None


def test_black_pawn_can_double_step_on_first_move():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    _change_turn_to_black(m)
    pawn = board.get_figure_at(0, 6)

    ok = m.move(pawn, 0, 4)

    assert ok is True
    assert board.get_figure_at(0, 4) is pawn
    assert board.get_figure_at(0, 6) is None


def test_black_pawn_can_capture_diagonally():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    white_target = board.get_figure_at(2, 1)
    board.move(white_target, 0, 5)

    _change_turn_to_black(m)
    black_pawn = board.get_figure_at(1, 6)

    ok = m.move(black_pawn, 0, 5)

    assert ok is True
    assert board.get_figure_at(0, 5) is black_pawn
    assert white_target not in board.get_figures()


def test_black_pawn_cannot_advance_when_blocked():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    blocker = board.get_figure_at(1, 0)
    board.move(blocker, 0, 5)

    _change_turn_to_black(m)
    black_pawn = board.get_figure_at(0, 6)

    assert m.move(black_pawn, 0, 5) is False
    assert m.move(black_pawn, 0, 4) is False
    assert board.get_figure_at(0, 6) is black_pawn


def test_black_pawn_cannot_move_backwards():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    black_pawn = board.get_figure_at(0, 6)
    board.move(black_pawn, 0, 4)

    _change_turn_to_black(m)

    ok = m.move(black_pawn, 0, 5)

    assert ok is False
    assert board.get_figure_at(0, 4) is black_pawn
