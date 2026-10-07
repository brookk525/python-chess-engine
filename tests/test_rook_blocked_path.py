from model.match import Match
from model.enums import Color


def test_rook_cannot_move_through_pieces_but_can_move_until_block():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    rook = board.get_figure_at(0, 0)
    assert rook is not None
    assert rook.__class__.__name__ == "Rook"
    assert rook.get_color() == Color.WHITE

    # Setup: quitar el peón blanco de delante para poder mover la torre
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    board.move(pawn, 1, 2)

    # Colocar un bloqueador en la misma columna (0,4)
    blocker = board.get_figure_at(1, 0)  # Knight blanco
    assert blocker is not None
    board.move(blocker, 0, 4)

    # Camino: (0,1)(0,2)(0,3) libres, (0,4) ocupada por blocker
    assert board.get_figure_at(0, 1) is None
    assert board.get_figure_at(0, 2) is None
    assert board.get_figure_at(0, 3) is None
    assert board.get_figure_at(0, 4) is blocker

    # 1) Debe poder moverse justo antes del bloqueo
    ok1 = m.move(rook, 0, 3)
    assert ok1 is True
    assert (rook.get_x(), rook.get_y()) == (0, 3)
    assert board.get_figure_at(0, 3) is rook
    assert board.get_figure_at(0, 0) is None

    # Turno pasa a negras: mover un peón NEGRO que no interfiera con la casilla (0,5)
    black_pawn = board.get_figure_at(1, 6)
    assert black_pawn is not None
    assert black_pawn.__class__.__name__ == "Pawn"
    assert black_pawn.get_color() == Color.BLACK

    ok_black = m.move(black_pawn, 1, 5)
    assert ok_black is True

    # 2) Intentar saltar "más allá" del bloqueador: (0,3) -> (0,5) (bloqueador está en (0,4))
    rook_before = (rook.get_x(), rook.get_y())
    assert m.get_turn() == Color.WHITE

    ok2 = m.move(rook, 0, 5)

    assert ok2 is False
    assert m.get_turn() == Color.WHITE
    assert (rook.get_x(), rook.get_y()) == rook_before
    assert board.get_figure_at(0, 3) is rook
