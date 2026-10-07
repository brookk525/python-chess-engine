from dataclasses import dataclass

from model.match import Match
from model.enums import Color
from model.rook import Rook


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


def test_move_with_none_piece_fails_without_changing_state():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    turn_before = m.get_turn()
    board_before = _snapshot_board(board)

    ok = m.move(None, 0, 0)

    assert ok is False
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before


def test_move_with_piece_not_on_board_fails_without_changing_state():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board
    turn_before = m.get_turn()
    board_before = _snapshot_board(board)

    # Pieza "inventada": existe como objeto, pero NO está añadida al tablero
    rogue = Rook(0, 0, Color.WHITE)

    ok = m.move(rogue, 0, 1)

    assert ok is False
    assert m.get_turn() == turn_before
    assert _snapshot_board(board) == board_before
