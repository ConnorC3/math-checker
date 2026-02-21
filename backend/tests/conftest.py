"""
Shared pytest fixtures for the math validator test suite.

Run the full suite with:
    pytest tests/ -v

Or a single file:
    pytest tests/test_validator.py -v
"""

import pytest
from sympy import Symbol

@pytest.fixture
def x():
    return Symbol('x')

@pytest.fixture
def t():
    return Symbol('t')

@pytest.fixture
def C():
    return Symbol('C')
