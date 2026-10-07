from dataclasses import dataclass

from model.match import Match
from model.enums import Color


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


def test_white_pawn_cannot_move_forward_if_blocked_in_front():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board

    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Pone un bloqueador justo delante (0,2) moviendo una pieza existente del tablero
    blocker = board.get_figure_at(1, 0)  # Knight blanco de inicio
    assert blocker is not None
    board.move(blocker, 0, 2)
    assert board.get_figure_at(0, 2) is blocker

    turn_before = m.get_turn()
    board_before = _snapshot_board(board)

    # No debe poder avanzar 1
    ok1 = m.move(pawn, 0, 2)
    assert ok1 is False

    # Tampoco debe poder hacer doble paso desde inicio
    ok2 = m.move(pawn, 0, 3)
    assert ok2 is False

    # Estado intacto
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before
    assert board.get_figure_at(0, 1) is pawn
