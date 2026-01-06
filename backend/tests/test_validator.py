from app.core.parser import parse_equation
from app.core.validator import find_first_error
from app.core.algebra import equations_equal
from sympy import Eq, symbols, sin, cos

##### Test equations_equal  #####

x, y = symbols("x y")

def test_basic_valid_equation():
    eq1 = Eq(2*x + 3, 7)
    eq2 = Eq(2*x, 4)
    assert equations_equal(eq1, eq2)  # valid linear algebra step

def test_basic_invalid_equation():
    eq1 = Eq(2*x + 3, 7)
    eq2 = Eq(2*x, 5)
    assert not equations_equal(eq1, eq2)  # deliberately wrong

def test_simplification_equivalence():
    # Different forms but equivalent
    eq1 = Eq((x + 1)**2, x**2 + 2*x + 1)
    eq2 = Eq(x**2 + 2*x + 1, (x + 1)**2)
    assert equations_equal(eq1, eq2)

### Not testing multivariable equations right now

# def test_multiple_variables_valid():
#     eq1 = Eq(2*x + 3*y, 5)
#     eq2 = Eq(2*x, 5 - 3*y)
#     assert equations_equal(eq1, eq2)

# def test_multiple_variables_invalid():
#     eq1 = Eq(2*x + 3*y, 5)
#     eq2 = Eq(2*x, 5 - 2*y)  # wrong coefficient
#     assert not equations_equal(eq1, eq2)

def test_trivial_case():
    eq1 = Eq(x, x, evaluate=False)
    eq2 = Eq(x, x, evaluate=False)
    assert equations_equal(eq1, eq2)

def test_constant_equation():
    eq1 = Eq(3, 3, evaluate=False)
    eq2 = Eq(3, 3, evaluate=False)
    assert equations_equal(eq1, eq2)

def test_constant_mismatch():
    eq1 = Eq(3, 3, evaluate=False)
    eq2 = Eq(3, 4, evaluate=False)
    assert not equations_equal(eq1, eq2)

# def test_nested_expression_equivalence():
#     eq1 = Eq((x + y)**2, x**2 + 2*x*y + y**2)
#     eq2 = Eq(x**2 + 2*x*y + y**2, (x + y)**2)
#     assert equations_equal(eq1, eq2)

def test_trig_equation():
    eq1 = Eq(sin(x)**2 + cos(x)**2, 1, evaluate=False)
    eq2 = Eq(1, 1, evaluate=False)
    assert equations_equal(eq1, eq2)

##### Test find_first_error #####

def test_valid_solution():
    equations = [
        parse_equation("2*x + 3 = 7"),
        parse_equation("2*x = 4"),
        parse_equation("x = 2"),
    ]

    assert find_first_error(equations) is None

def test_invalid_solution():
    equations = [
        parse_equation("2*x + 3 = 7"),
        parse_equation("2*x = 5"),
        parse_equation("x = 2"),
    ]

    assert find_first_error(equations) == 1
