from model.match_service import MatchService
from model.enums import MatchState


def test_match_service_start_changes_waiting_to_running_and_is_idempotent():
    service = MatchService()
    match_id = service.create_match("p1", "p2")

    m = service.get_match(match_id)
    assert m is not None
    assert m.get_match_state() == MatchState.WAITING

    ok1 = service.start(match_id)
    assert ok1 is True
    assert m.get_match_state() == MatchState.RUNNING

    # Llamar start otra vez no debería hacer nada
    ok2 = service.start(match_id)
    assert ok2 is False
    assert m.get_match_state() == MatchState.RUNNING


def test_match_service_start_invalid_id_returns_false():
    service = MatchService()
    ok = service.start(9999)
    assert ok is False
