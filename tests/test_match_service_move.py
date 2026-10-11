from services.match_service import MatchService
from model.enums import Color


def test_match_service_move_applies_move_on_match_board():
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

    ok = service.move(match_id, pawn, 0, 2)

    assert ok is True
    assert board.get_figure_at(0, 2) is pawn
    assert (pawn.get_x(), pawn.get_y()) == (0, 2)


def test_match_service_move_invalid_id_returns_false():
    service = MatchService()
    ok = service.move(9999, None, 0, 0)
    assert ok is False
