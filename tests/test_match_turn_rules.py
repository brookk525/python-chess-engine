from model.match import Match
from model.enums import Color


def test_match_start_turn_is_white():
    m = Match(1, "p1", "p2")
    m.start()
    assert m.get_turn() == Color.WHITE


def test_cannot_move_black_piece_on_white_turn():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board

    black_pawn = board.get_figure_at(0, 6)
    assert black_pawn is not None
    assert black_pawn.get_color() == Color.BLACK

    # Intento de movimiento típico de peón negro (hacia y-1)
    ok = m.move(black_pawn, 0, 5)

    assert ok is False
    assert m.get_turn() == Color.WHITE

    # La pieza no se ha movido
    assert black_pawn.get_x() == 0
    assert black_pawn.get_y() == 6
    assert board.get_figure_at(0, 6) is black_pawn
