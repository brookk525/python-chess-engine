from dataclasses import dataclass

from model.match_service import MatchService
from model.enums import Color


@dataclass(frozen=True)
class PiecePojo:
    piece_type: str
    color: str
    x: int
    y: int


def snapshot_board(board) -> set[PiecePojo]:
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


def test_service_move_invalid_does_not_change_board_or_turn():
    service = MatchService()
    match_id = service.create_match("p1", "p2")
    assert service.start(match_id) is True

    m = service.get_match(match_id)
    assert m is not None
    board = m._board

    turn_before = m.get_turn()
    board_before = snapshot_board(board)

    # Movimiento ilegal: peón blanco intenta moverse 3 casillas
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    ok = service.move(match_id, pawn, 0, 4)

    assert ok is False
    assert m.get_turn() == turn_before
    assert snapshot_board(board) == board_before
