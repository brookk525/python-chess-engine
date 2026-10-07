from model.match import Match
from model.enums import Color


def test_king_can_move_one_square():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    assert king is not None
    assert king.__class__.__name__ == "King"
    assert king.get_color() == Color.WHITE

    # Liberar la casilla (4,1) moviendo el peón blanco que bloquea
    pawn = board.get_figure_at(4, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    board.move(pawn, 4, 2)

    ok = m.move(king, 4, 1)

    assert ok is True
    assert (king.get_x(), king.get_y()) == (4, 1)
    assert board.get_figure_at(4, 1) is king
    assert board.get_figure_at(4, 0) is None


def test_king_cannot_move_two_squares_like_long_move():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    assert king is not None
    assert king.__class__.__name__ == "King"
    assert king.get_color() == Color.WHITE

    # Intento ilegal: mover 2 casillas en la misma fila (sin enroque)
    ok = m.move(king, 6, 0)

    assert ok is False
    assert (king.get_x(), king.get_y()) == (4, 0)
    assert board.get_figure_at(4, 0) is king
