from model.match import Match
from model.enums import Color


def test_queen_can_move_straight_like_rook_when_path_is_free():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    queen = board.get_figure_at(3, 0)
    assert queen is not None
    assert queen.__class__.__name__ == "Queen"
    assert queen.get_color() == Color.WHITE

    # Liberar la columna moviendo el peón de delante (3,1)
    pawn = board.get_figure_at(3, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    board.move(pawn, 3, 3)

    ok = m.move(queen, 3, 2)

    assert ok is True
    assert (queen.get_x(), queen.get_y()) == (3, 2)
    assert board.get_figure_at(3, 2) is queen
    assert board.get_figure_at(3, 0) is None


def test_queen_can_move_diagonally_like_bishop_when_path_is_free():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    queen = board.get_figure_at(3, 0)
    assert queen is not None
    assert queen.__class__.__name__ == "Queen"
    assert queen.get_color() == Color.WHITE

    # Liberar la diagonal moviendo el peón de (4,1)
    pawn = board.get_figure_at(4, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    board.move(pawn, 4, 2)

    # Movimiento diagonal válido: (3,0) -> (5,2)
    ok = m.move(queen, 5, 2)

    assert ok is True
    assert (queen.get_x(), queen.get_y()) == (5, 2)
    assert board.get_figure_at(5, 2) is queen
    assert board.get_figure_at(3, 0) is None


def test_queen_cannot_move_like_knight():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    queen = board.get_figure_at(3, 0)
    assert queen is not None
    assert queen.__class__.__name__ == "Queen"
    assert queen.get_color() == Color.WHITE

    # Movimiento tipo "L" de caballo (3,0) -> (4,2)
    ok = m.move(queen, 4, 2)

    assert ok is False
    assert (queen.get_x(), queen.get_y()) == (3, 0)
    assert board.get_figure_at(3, 0) is queen
