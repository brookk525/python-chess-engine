from model.match import Match
from model.enums import Color


def test_bishop_can_move_diagonally_when_path_is_free():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    # Alfil blanco inicial en (2,0)
    bishop = board.get_figure_at(2, 0)
    assert bishop is not None
    assert bishop.__class__.__name__ == "Bishop"
    assert bishop.get_color() == Color.WHITE

    # Liberar la diagonal (3,1) moviendo el peón que bloquea
    pawn = board.get_figure_at(3, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    board.move(pawn, 3, 2)

    # Movimiento diagonal válido: (2,0) -> (4,2)
    ok = m.move(bishop, 4, 2)

    assert ok is True
    assert (bishop.get_x(), bishop.get_y()) == (4, 2)
    assert board.get_figure_at(4, 2) is bishop
    assert board.get_figure_at(2, 0) is None


def test_bishop_cannot_move_like_rook():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    bishop = board.get_figure_at(2, 0)
    assert bishop is not None
    assert bishop.__class__.__name__ == "Bishop"
    assert bishop.get_color() == Color.WHITE

    # Intento ilegal: misma columna (2,0) -> (2,2)
    ok = m.move(bishop, 2, 2)

    assert ok is False
    assert (bishop.get_x(), bishop.get_y()) == (2, 0)
    assert board.get_figure_at(2, 0) is bishop


def test_bishop_cannot_jump_over_blocking_piece_on_diagonal():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    bishop = board.get_figure_at(2, 0)
    assert bishop is not None
    assert bishop.__class__.__name__ == "Bishop"
    assert bishop.get_color() == Color.WHITE

    # Dejar el peón en (3,1) como bloqueador y tentar saltar por encima hasta (4,2)
    blocker = board.get_figure_at(3, 1)
    assert blocker is not None
    assert blocker.__class__.__name__ == "Pawn"
    assert blocker.get_color() == Color.WHITE

    ok = m.move(bishop, 4, 2)

    assert ok is False
    assert (bishop.get_x(), bishop.get_y()) == (2, 0)
    assert board.get_figure_at(2, 0) is bishop
    assert board.get_figure_at(3, 1) is blocker
