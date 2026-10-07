from model.match import Match
from model.enums import Color


def test_capture_enemy_piece_removes_it_and_moves_attacker():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    # --- Setup simple: torre blanca puede capturar una negra en misma columna sin piezas en medio ---
    rook = board.get_figure_at(0, 0)
    assert rook is not None
    assert rook.__class__.__name__ == "Rook"
    assert rook.get_color() == Color.WHITE

    # Quitar el peón blanco de la columna 0 (está en 0,1) para que no bloquee
    white_pawn = board.get_figure_at(0, 1)
    assert white_pawn is not None
    assert white_pawn.__class__.__name__ == "Pawn"
    board.move(white_pawn, 1, 2)  # movimiento "de setup" (directo en board)

    # Poner la torre en una posición cómoda
    board.move(rook, 0, 3)

    # Colocar una pieza negra en la misma columna (0,5) sin nada entre medias
    black_pawn = board.get_figure_at(0, 6)
    assert black_pawn is not None
    assert black_pawn.__class__.__name__ == "Pawn"
    assert black_pawn.get_color() == Color.BLACK
    board.move(black_pawn, 0, 5)

    # Confirmar línea libre entre (0,3) y (0,5)
    assert board.get_figure_at(0, 4) is None
    assert board.get_figure_at(0, 5) is black_pawn

    # --- Captura real usando Match.move (la que debe validar reglas) ---
    turn_before = m.get_turn()
    assert turn_before == Color.WHITE

    ok = m.move(rook, 0, 5)

    assert ok is True
    assert rook.get_x() == 0
    assert rook.get_y() == 5
    assert board.get_figure_at(0, 5) is rook
    assert board.get_figure_at(0, 3) is None

    # La pieza negra ya no debe estar en el tablero
    assert black_pawn not in board.get_figures()


def test_cannot_capture_ally_piece_and_state_does_not_change():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    rook = board.get_figure_at(0, 0)
    assert rook is not None
    assert rook.__class__.__name__ == "Rook"
    assert rook.get_color() == Color.WHITE

    # Liberar columna y preparar destino con aliado
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Mover torre a (0,3)
    board.move(pawn, 1, 2)     # quita el peón de delante
    board.move(rook, 0, 3)

    # Poner un aliado en (0,5) (mismo color)
    board.move(pawn, 0, 5)

    assert m.get_turn() == Color.WHITE
    rook_x_before, rook_y_before = rook.get_x(), rook.get_y()
    pawn_x_before, pawn_y_before = pawn.get_x(), pawn.get_y()

    ok = m.move(rook, 0, 5)

    assert ok is False
    assert m.get_turn() == Color.WHITE  # no cambia turno en movimiento inválido

    # Ambas piezas siguen igual
    assert (rook.get_x(), rook.get_y()) == (rook_x_before, rook_y_before)
    assert (pawn.get_x(), pawn.get_y()) == (pawn_x_before, pawn_y_before)
    assert board.get_figure_at(0, 3) is rook
    assert board.get_figure_at(0, 5) is pawn
