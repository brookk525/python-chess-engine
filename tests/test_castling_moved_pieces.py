from model.match import Match
from model.enums import Color
from model.pawn import Pawn


def _keep_only(board, keep):
    for fig in list(board.get_figures()):
        if fig not in keep:
            board._remove_figure(fig)


def _add_black_dummy_pawn(board):
    # Peón negro dummy para poder alternar turno sin tocar piezas del enroque
    dummy = Pawn(1, 6, Color.BLACK)
    board._add_figure(dummy)
    return dummy


def test_castling_fails_if_king_has_moved_before():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    # Tablero simple: rey + torre + un peón negro dummy para alternar turno
    _keep_only(board, {king, rook})
    dummy = _add_black_dummy_pawn(board)

    # Simular que el rey ya se movió: moverlo 1 casilla y devolverlo (respetando turnos)
    ok1 = m.move(king, 4, 1)
    assert ok1 is True
    ok_dummy1 = m.move(dummy, 1, 5)
    assert ok_dummy1 is True

    ok2 = m.move(king, 4, 0)
    assert ok2 is True
    ok_dummy2 = m.move(dummy, 1, 4)
    assert ok_dummy2 is True

    assert m.get_turn() == Color.WHITE

    ok_castle = m.move(king, 6, 0)

    assert ok_castle is False
    assert (king.get_x(), king.get_y()) == (4, 0)
    assert (rook.get_x(), rook.get_y()) == (7, 0)


def test_castling_fails_if_rook_has_moved_before():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    _keep_only(board, {king, rook})
    dummy = _add_black_dummy_pawn(board)

    # Simular que la torre ya se movió: moverla y devolverla (respetando turnos)
    ok1 = m.move(rook, 7, 1)
    assert ok1 is True
    ok_dummy1 = m.move(dummy, 1, 5)
    assert ok_dummy1 is True

    ok2 = m.move(rook, 7, 0)
    assert ok2 is True
    ok_dummy2 = m.move(dummy, 1, 4)
    assert ok_dummy2 is True

    assert m.get_turn() == Color.WHITE

    ok_castle = m.move(king, 6, 0)

    assert ok_castle is False
    assert (king.get_x(), king.get_y()) == (4, 0)
    assert (rook.get_x(), rook.get_y()) == (7, 0)
