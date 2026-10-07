from model.match import Match
from model.enums import Color


def test_turn_changes_after_valid_move():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    ok = m.move(pawn, 0, 2)

    assert ok is True
    assert m.get_turn() == Color.BLACK


def test_turn_does_not_change_after_invalid_move():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Movimiento inválido típico: un peón no puede saltar 3 casillas
    ok = m.move(pawn, 0, 4)

    assert ok is False
    assert m.get_turn() == Color.WHITE
