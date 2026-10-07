from dataclasses import dataclass

from model.match_service import MatchService
from model.enums import Color, MatchState, PromotingType


@dataclass(frozen=True)
class PiecePojo:
    piece_type: str
    color: str
    x: int
    y: int


def _snapshot_board(board) -> set[PiecePojo]:
    snap: set[PiecePojo] = set()
    for fig in board.get_figures():
        snap.add(
            PiecePojo(
                fig.__class__.__name__,
                fig.get_color().value,
                fig.get_x(),
                fig.get_y(),
            )
        )
    return snap


def test_match_service_promote_replaces_pawn_and_returns_to_running():
    service = MatchService()
    match_id = service.create_match("p1", "p2")
    assert service.start(match_id) is True

    m = service.get_match(match_id)
    assert m is not None
    board = m._board

    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Limpiar destino de promoción (quitar piezas negras en la columna 0 arriba)
    black_pawn = board.get_figure_at(0, 6)
    if black_pawn is not None:
        board._remove_figure(black_pawn)
    black_back = board.get_figure_at(0, 7)
    if black_back is not None:
        board._remove_figure(black_back)

    # A casilla de coronar y coronar
    board.move(pawn, 0, 6)
    ok = service.move(match_id, pawn, 0, 7)
    assert ok is True
    assert m.get_match_state() == MatchState.WAITING_PROMOTION
    assert m.get_turn() == Color.WHITE

    # Nota: en tu MatchService.promote() parece que NO devuelve bool (devuelve None),
    # así que aquí validamos por efectos en el estado/tablero
    service.promote(match_id, PromotingType.QUEEN)

    assert m.get_match_state() == MatchState.RUNNING
    assert m.get_turn() == Color.BLACK

    new_piece = board.get_figure_at(0, 7)
    assert new_piece is not None
    assert new_piece.__class__.__name__ == "Queen"
    assert new_piece.get_color() == Color.WHITE

    assert pawn not in board.get_figures()


def test_match_service_promote_when_not_waiting_promotion_does_not_change_state():
    service = MatchService()
    match_id = service.create_match("p1", "p2")
    assert service.start(match_id) is True

    m = service.get_match(match_id)
    assert m is not None
    board = m._board

    state_before = m.get_match_state()
    turn_before = m.get_turn()
    board_before = _snapshot_board(board)

    service.promote(match_id, PromotingType.QUEEN)

    assert m.get_match_state() == state_before
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before
