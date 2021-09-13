import pytest

from solver.solver import Solver

_solver = Solver()

@pytest.fixture
def solver():
    return _solver

def test_oh_5c6dAcAsQs(solver):
    assert solver.process("omaha-holdem 5c6dAcAsQs TsQh9hQc 8d7cTcJd 5s5d7s4d Qd3cKs4c KdJs2hAh Kh4hKc7h 6h7d2cJc") == "8d7cTcJd 6h7d2cJc Qd3cKs4c Kh4hKc7h KdJs2hAh 5s5d7s4d TsQh9hQc"

def test_oh_3d4s5dJsQd(solver):
    assert solver.process("omaha-holdem 3d4s5dJsQd 8s2h6s8h 7cThKs5s 5hJh2s7d 8d9s5c4h 7sJdKcAs 9h7h2dTc Qh8cTsJc") == "9h7h2dTc 7cThKs5s 7sJdKcAs 8d9s5c4h 5hJh2s7d Qh8cTsJc 8s2h6s8h"

def test_oh_3d3s4d6hJc(solver):
    assert solver.process("omaha-holdem 3d3s4d6hJc Js2dKd8c KsAsTcTs Jh2h3c9c Qc8dAd6c 7dQsAc5d") == "Qc8dAd6c KsAsTcTs Js2dKd8c 7dQsAc5d Jh2h3c9c"
