from app.core.models import AlgebraStep
from app.core.parser import parse_equation
from app.core.validator import find_first_error

##### Test find_first_error #####

def test_valid_solution():
    equations = [
        AlgebraStep(parse_equation("2*x + 3 = 7")),
        AlgebraStep(parse_equation("2*x = 4")),
        AlgebraStep(parse_equation("x = 2")),
    ]

    assert find_first_error(equations) is None

def test_invalid_solution():
    equations = [
        AlgebraStep(parse_equation("2*x + 3 = 7")),
        AlgebraStep(parse_equation("2*x = 5")),
        AlgebraStep(parse_equation("x = 2")),
    ]

    assert find_first_error(equations) == 1
