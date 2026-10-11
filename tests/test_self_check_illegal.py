from model.match import Match
from model.enums import Color
from model.figures.rook import Rook


def _keep_only(board, keep):
    for fig in list(board.get_figures()):
        if fig not in keep:
            board._remove_figure(fig)


def test_move_is_illegal_if_it_leaves_own_king_in_check():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    # Rey blanco en su posición inicial
    king = board.get_figure_at(4, 0)
    assert king is not None
    assert king.__class__.__name__ == "King"
    assert king.get_color() == Color.WHITE

    # Pieza blanca que bloquea el jaque: usamos una torre blanca como "escudo"
    blocker = board.get_figure_at(0, 0)
    assert blocker is not None
    assert blocker.__class__.__name__ == "Rook"
    assert blocker.get_color() == Color.WHITE

    # Torre negra que apunta al rey por la columna x=4
    enemy_rook = Rook(4, 7, Color.BLACK)

    # Tablero simple: rey + escudo + torre enemiga
    _keep_only(board, {king, blocker})
    board._add_figure(enemy_rook)

    # Colocar el escudo en la misma columna, entre la torre enemiga y el rey
    board.move(blocker, 4, 1)
    assert board.get_figure_at(4, 1) is blocker
    assert board.get_figure_at(4, 7) is enemy_rook

    # Intento mover el escudo fuera de la columna para dejar la línea libre -> debería ser ilegal
    assert m.get_turn() == Color.WHITE
    blocker_before = (blocker.get_x(), blocker.get_y())

    ok = m.move(blocker, 5, 1)  # movimiento válido para torre, pero dejaría al rey en jaque

    assert ok is False
    assert m.get_turn() == Color.WHITE
    assert (blocker.get_x(), blocker.get_y()) == blocker_before
    assert board.get_figure_at(4, 1) is blocker
