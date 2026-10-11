from model.match import Match
from model.enums import Color
from model.figures.rook import Rook


def _keep_only(board, keep):
    for fig in list(board.get_figures()):
        if fig not in keep:
            board._remove_figure(fig)


def test_castling_fails_when_piece_between_king_and_rook():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)
    blocker = board.get_figure_at(6, 0)  # Knight blanco inicial

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE
    assert blocker is not None and blocker.__class__.__name__ == "Knight" and blocker.get_color() == Color.WHITE

    # Dejar solo rey, torre y un bloqueador en medio (en 5,0)
    _keep_only(board, {king, rook, blocker})
    board.move(blocker, 5, 0)

    king_before = (king.get_x(), king.get_y())
    rook_before = (rook.get_x(), rook.get_y())
    assert m.get_turn() == Color.WHITE

    ok = m.move(king, 6, 0)  # enroque corto

    assert ok is False
    assert m.get_turn() == Color.WHITE
    assert (king.get_x(), king.get_y()) == king_before
    assert (rook.get_x(), rook.get_y()) == rook_before
    assert board.get_figure_at(4, 0) is king
    assert board.get_figure_at(7, 0) is rook
    assert board.get_figure_at(5, 0) is blocker


def test_castling_fails_when_king_is_in_check():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    # Solo rey + torre + una torre negra que da jaque directo por la columna del rey
    enemy_rook = Rook(4, 7, Color.BLACK)
    _keep_only(board, {king, rook})
    board._add_figure(enemy_rook)

    king_before = (king.get_x(), king.get_y())
    rook_before = (rook.get_x(), rook.get_y())
    assert m.get_turn() == Color.WHITE

    ok = m.move(king, 6, 0)  # intenta enroque corto estando en jaque

    assert ok is False
    assert m.get_turn() == Color.WHITE
    assert (king.get_x(), king.get_y()) == king_before
    assert (rook.get_x(), rook.get_y()) == rook_before
    assert board.get_figure_at(4, 0) is king
    assert board.get_figure_at(7, 0) is rook


def test_castling_fails_when_square_king_passes_through_is_attacked():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    # Enroque corto: el rey pasa por (5,0). Ponemos una torre negra atacando esa casilla.
    # Importante: que NO dé jaque al rey en (4,0), solo ataque (5,0)
    enemy_rook = Rook(5, 7, Color.BLACK)

    _keep_only(board, {king, rook})
    board._add_figure(enemy_rook)

    # Asegurar que el camino del enroque está libre
    assert board.get_figure_at(5, 0) is None
    assert board.get_figure_at(6, 0) is None
    assert m.get_turn() == Color.WHITE

    king_before = (king.get_x(), king.get_y())
    rook_before = (rook.get_x(), rook.get_y())

    ok = m.move(king, 6, 0)

    assert ok is False
    assert m.get_turn() == Color.WHITE
    assert (king.get_x(), king.get_y()) == king_before
    assert (rook.get_x(), rook.get_y()) == rook_before
    assert board.get_figure_at(4, 0) is king
    assert board.get_figure_at(7, 0) is rook


def test_castling_fails_when_rook_square_contains_another_ally_piece():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    knight = board.get_figure_at(6, 0)

    # Eliminamos el resto de piezas y colocamos el caballo donde debería estar
    # la torre del enroque corto.
    _keep_only(board, {king, knight})
    board.move(knight, 7, 0)

    king_before = (king.get_x(), king.get_y())
    knight_before = (knight.get_x(), knight.get_y())

    ok = m.move(king, 6, 0)

    assert ok is False
    assert m.get_turn() == Color.WHITE
    assert (king.get_x(), king.get_y()) == king_before
    assert (knight.get_x(), knight.get_y()) == knight_before
