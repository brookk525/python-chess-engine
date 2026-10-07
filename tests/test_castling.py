from model.match import Match
from model.enums import Color


def _keep_only(board, keep):
    # keep: set of figure objects to keep
    for fig in list(board.get_figures()):
        if fig not in keep:
            board._remove_figure(fig)


def test_white_can_castle_kingside_when_path_is_clear_and_not_in_check():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(7, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    # Tablero simple: solo rey + torre derecha
    _keep_only(board, {king, rook})

    assert board.get_figure_at(5, 0) is None
    assert board.get_figure_at(6, 0) is None
    assert m.get_turn() == Color.WHITE

    ok = m.move(king, 6, 0)  # enroque corto

    assert ok is True
    assert (king.get_x(), king.get_y()) == (6, 0)
    assert (rook.get_x(), rook.get_y()) == (5, 0)
    assert board.get_figure_at(6, 0) is king
    assert board.get_figure_at(5, 0) is rook


def test_white_can_castle_queenside_when_path_is_clear_and_not_in_check():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    king = board.get_figure_at(4, 0)
    rook = board.get_figure_at(0, 0)

    assert king is not None and king.__class__.__name__ == "King" and king.get_color() == Color.WHITE
    assert rook is not None and rook.__class__.__name__ == "Rook" and rook.get_color() == Color.WHITE

    # Tablero simple: solo rey + torre izquierda
    _keep_only(board, {king, rook})

    assert board.get_figure_at(1, 0) is None
    assert board.get_figure_at(2, 0) is None
    assert board.get_figure_at(3, 0) is None
    assert m.get_turn() == Color.WHITE

    ok = m.move(king, 2, 0)  # enroque largo

    assert ok is True
    assert (king.get_x(), king.get_y()) == (2, 0)
    assert (rook.get_x(), rook.get_y()) == (3, 0)
    assert board.get_figure_at(2, 0) is king
    assert board.get_figure_at(3, 0) is rook
