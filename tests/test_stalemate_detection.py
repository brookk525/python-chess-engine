from model.match import Match
from model.enums import Color
from model.figures.king import King
from model.figures.queen import Queen


def _clear_board(board):
    for fig in list(board.get_figures()):
        board._remove_figure(fig)


def test_is_stalemate_true_for_simple_stalemate_position():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    _clear_board(board)

    # Ahogado típico:
    # Rey blanco en a1 (0,0) SIN jaque, pero sin movimientos legales (a2, b1, b2 controladas)
    white_king = King(0, 0, Color.WHITE)

    # Rey negro lejos (no es estrictamente necesario en algunos motores, pero lo ponemos por seguridad)
    black_king = King(2, 2, Color.BLACK)

    # Reina negra en c2 (2,1) controla a2 (0,1), b1 (1,0) y b2 (1,1)
    black_queen = Queen(2, 1, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_king)
    board._add_figure(black_queen)

    # No está en jaque, pero sí es ahogado
    assert m.is_in_check(Color.WHITE, board) is False
    assert m.is_stalemate(Color.WHITE, board) is True


def test_is_stalemate_false_when_king_has_a_legal_move():
    m = Match(1, "p1", "p2")
    m.start()
    board = m._board
    _clear_board(board)

    white_king = King(0, 0, Color.WHITE)
    black_king = King(2, 2, Color.BLACK)

    # Movemos la reina a c4 (2,3): sigue presionando, pero deja b1 (1,0) como casilla segura
    black_queen = Queen(2, 3, Color.BLACK)

    board._add_figure(white_king)
    board._add_figure(black_king)
    board._add_figure(black_queen)

    assert m.is_in_check(Color.WHITE, board) is False
    assert m.is_stalemate(Color.WHITE, board) is False
