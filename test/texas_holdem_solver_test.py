import pytest

from solver.solver import Solver

_solver = Solver()

@pytest.fixture
def solver():
    return _solver

def test_th_5c6dAcAsQs(solver):
    assert solver.process("texas-holdem 5c6dAcAsQs Ks4c KdJs 2hAh Kh4h Kc7h 6h7d 2cJc") == "2cJc Kh4h=Ks4c Kc7h KdJs 6h7d 2hAh"

def test_th_2h5c8sAsKc(solver):
    assert solver.process("texas-holdem 2h5c8sAsKc Qs9h KdQh 3cKh Jc6s") == "Jc6s Qs9h 3cKh KdQh"

def test_th_3d4s5dJsQd(solver):
    assert solver.process("texas-holdem 3d4s5dJsQd 5c4h 7sJd KcAs 9h7h 2dTc Qh8c TsJc") == "9h7h 2dTc KcAs 7sJd TsJc Qh8c 5c4h"
