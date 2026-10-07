from model.match import Match
from model.enums import Color, MatchState, PromotingType


def test_pawn_reaching_last_rank_sets_waiting_promotion_and_turn_does_not_change():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    # Cogemos un peón blanco
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Limpiamos la columna 0 en la zona de promoción (quitamos piezas negras que estorban)
    black_pawn = board.get_figure_at(0, 6)
    if black_pawn is not None:
        board._remove_figure(black_pawn)

    black_back = board.get_figure_at(0, 7)
    if black_back is not None:
        board._remove_figure(black_back)

    # Ponemos el peón a una casilla de coronar (y=6)
    board.move(pawn, 0, 6)
    assert m.get_match_state() == MatchState.RUNNING
    assert m.get_turn() == Color.WHITE

    # Movimiento final: coronar (y=7)
    ok = m.move(pawn, 0, 7)

    assert ok is True
    assert (pawn.get_x(), pawn.get_y()) == (0, 7)
    assert m.get_match_state() == MatchState.WAITING_PROMOTION
    # No cambia turno todavía
    assert m.get_turn() == Color.WHITE


def test_promote_replaces_pawn_and_returns_to_running_and_changes_turn():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Limpiar destino de promoción
    black_pawn = board.get_figure_at(0, 6)
    if black_pawn is not None:
        board._remove_figure(black_pawn)

    black_back = board.get_figure_at(0, 7)
    if black_back is not None:
        board._remove_figure(black_back)

    # A una casilla de coronar y coronar con move()
    board.move(pawn, 0, 6)
    ok = m.move(pawn, 0, 7)
    assert ok is True
    assert m.get_match_state() == MatchState.WAITING_PROMOTION
    assert m.get_turn() == Color.WHITE

    # Promocionar a reina
    m.promote(PromotingType.QUEEN)

    assert m.get_match_state() == MatchState.RUNNING
    assert m.get_turn() == Color.BLACK

    new_piece = board.get_figure_at(0, 7)
    assert new_piece is not None
    assert new_piece.__class__.__name__ == "Queen"
    assert new_piece.get_color() == Color.WHITE

    # El peón original ya no debe existir en el tablero
    assert pawn not in board.get_figures()


def test_promote_with_invalid_type_keeps_pawn_waiting():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    pawn = board.get_figure_at(0, 1)
    black_pawn = board.get_figure_at(0, 6)
    black_back = board.get_figure_at(0, 7)

    board._remove_figure(black_pawn)
    board._remove_figure(black_back)
    board.move(pawn, 0, 6)

    ok = m.move(pawn, 0, 7)

    assert ok is True
    assert m.get_match_state() == MatchState.WAITING_PROMOTION

    m.promote(None)

    assert m.get_match_state() == MatchState.WAITING_PROMOTION
    assert m.get_turn() == Color.WHITE
    assert board.get_figure_at(0, 7) is pawn
