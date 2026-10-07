import pytest
from model.match import Match

@pytest.fixture
def match():
    m = Match(0, "p1", "p2")
    m.start()
    return m