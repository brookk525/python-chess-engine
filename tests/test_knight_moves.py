from model.match import Match
from model.enums import Color


def test_knight_can_move_in_L_shape_from_start():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    # Caballo blanco inicial en (1,0)
    knight = board.get_figure_at(1, 0)
    assert knight is not None
    assert knight.__class__.__name__ == "Knight"
    assert knight.get_color() == Color.WHITE

    # Movimiento típico válido desde el inicio: (1,0) -> (2,2)
    ok = m.move(knight, 2, 2)

    assert ok is True
    assert (knight.get_x(), knight.get_y()) == (2, 2)
    assert board.get_figure_at(2, 2) is knight
    assert board.get_figure_at(1, 0) is None


def test_knight_cannot_move_onto_ally_square():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board

    knight = board.get_figure_at(1, 0)
    assert knight is not None
    assert knight.__class__.__name__ == "Knight"
    assert knight.get_color() == Color.WHITE

    # Queremos que (2,2) esté ocupada por una pieza blanca aliada
    ally = board.get_figure_at(0, 1)  # peón blanco
    assert ally is not None
    assert ally.__class__.__name__ == "Pawn"
    assert ally.get_color() == Color.WHITE

    # "Setup": mover el peón a (2,2) directamente en el board
    board.move(ally, 2, 2)
    assert board.get_figure_at(2, 2) is ally

    # Intento mover el caballo a una casilla con aliado
    turn_before = m.get_turn()
    knight_before = (knight.get_x(), knight.get_y())
    ally_before = (ally.get_x(), ally.get_y())

    ok = m.move(knight, 2, 2)

    assert ok is False
    assert m.get_turn() == turn_before

    # Ambos siguen igual
    assert (knight.get_x(), knight.get_y()) == knight_before
    assert (ally.get_x(), ally.get_y()) == ally_before
    assert board.get_figure_at(1, 0) is knight
    assert board.get_figure_at(2, 2) is ally
