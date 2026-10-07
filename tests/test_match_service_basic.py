from model.match_service import MatchService


def test_match_service_create_get_delete():
    service = MatchService()

    match_id = service.create_match("p1", "p2")
    assert match_id is not None

    m = service.get_match(match_id)
    assert m is not None
    assert m.get_id() == match_id

    ok = service.delete_match(match_id)
    assert ok is True

    m2 = service.get_match(match_id)
    assert m2 is None
