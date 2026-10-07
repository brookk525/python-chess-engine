from model.match import Match
from model.enums import Color


def test_white_pawn_can_advance_one_if_free():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)

    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    ok = m.move(pawn, 0, 2)

    assert ok is True
    assert pawn.get_x() == 0
    assert pawn.get_y() == 2
    assert board.get_figure_at(0, 2) is pawn
    assert board.get_figure_at(0, 1) is None


def test_white_pawn_can_double_step_on_first_move_if_path_free():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)

    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Doble paso desde la posición inicial (y=1 -> y=3)
    ok = m.move(pawn, 0, 3)

    assert ok is True
    assert pawn.get_x() == 0
    assert pawn.get_y() == 3
    assert board.get_figure_at(0, 3) is pawn
    assert board.get_figure_at(0, 1) is None


def test_white_pawn_cannot_double_step_after_it_has_moved():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)

    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Primero lo mueve 1 casilla
    ok1 = m.move(pawn, 0, 2)
    assert ok1 is True
    assert pawn.get_y() == 2

    # Turno pasa a negras: hace un movimiento legal para volver a blancas
    black_pawn = board.get_figure_at(1, 6)
    assert black_pawn is not None
    assert black_pawn.__class__.__name__ == "Pawn"
    assert black_pawn.get_color() == Color.BLACK

    ok_black = m.move(black_pawn, 1, 5)
    assert ok_black is True

    # Ahora vuelve a ser turno de blancas: intenta el "doble paso" (2 casillas) pero ya no debe poder
    ok2 = m.move(pawn, 0, 4)

    assert ok2 is False
    assert pawn.get_x() == 0
    assert pawn.get_y() == 2
    assert board.get_figure_at(0, 2) is pawn
