from dataclasses import dataclass

from model.match import Match
from model.enums import Color


@dataclass(frozen=True)
class PiecePojo:
    piece_type: str
    color: str
    x: int
    y: int


def _expected_initial_setup() -> set[PiecePojo]:
    expected: set[PiecePojo] = set()

    # Orden de piezas en la fila de atrás
    back_row = ["Rook", "Knight", "Bishop", "Queen", "King", "Bishop", "Knight", "Rook"]

    # Blancas
    for x in range(8):
        expected.add(PiecePojo("Pawn", Color.WHITE.value, x, 1))
        expected.add(PiecePojo(back_row[x], Color.WHITE.value, x, 0))

    # Negras
    for x in range(8):
        expected.add(PiecePojo("Pawn", Color.BLACK.value, x, 6))
        expected.add(PiecePojo(back_row[x], Color.BLACK.value, x, 7))

    return expected


def test_match_start_creates_all_pieces_in_correct_positions():
    m = Match(1, "p1", "p2")
    m.start()

    board = m._board  # en tu clase Match es _board (protegido), se puede leer para test

    assert board.get_figure_count() == 32

    actual: set[PiecePojo] = set()
    for fig in board.get_figures():
        actual.add(
            PiecePojo(
                fig.__class__.__name__,
                fig.get_color().value,
                fig.get_x(),
                fig.get_y(),
            )
        )

    expected = _expected_initial_setup()
    assert actual == expected
