from dataclasses import dataclass

from model.match import Match
from model.enums import MatchState, Color
from model.figures.rook import Rook


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


def test_cannot_move_when_match_state_is_waiting():
    # Sin start(): estado inicial debería ser WAITING
    m = Match(1, "p1", "p2")

    assert m.get_match_state() == MatchState.WAITING

    board = m._board
    turn_before = m.get_turn()
    board_before = _snapshot_board(board)

    # Intento mover una pieza "inventada" (ni siquiera está en el tablero)
    rogue = Rook(0, 0, Color.WHITE)
    ok = m.move(rogue, 0, 1)

    assert ok is False
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before


def test_cannot_move_when_match_state_is_waiting_promotion():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    pawn = board.get_figure_at(0, 1)
    assert pawn is not None
    assert pawn.__class__.__name__ == "Pawn"
    assert pawn.get_color() == Color.WHITE

    # Forzamos el estado a WAITING_PROMOTION para simular que está bloqueado por promoción
    m._state = MatchState.WAITING_PROMOTION

    turn_before = m.get_turn()
    board_before = _snapshot_board(board)
    pawn_before = (pawn.get_x(), pawn.get_y())

    ok = m.move(pawn, 0, 2)

    assert ok is False
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before
    assert (pawn.get_x(), pawn.get_y()) == pawn_before
