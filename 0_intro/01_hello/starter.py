"""
>>> add(2, 3)
5

>>> add(10, 5)
15

>>> multiply(2, 3)
6

>>> multiply(10, 5)
50

>>> add(0, 0)
0

>>> multiply(1, 1)
1
"""

# %% About
# - Name: Intro - Simple Calculator
# - Difficulty: easy
# - Lines: 4
# - Focus: Setup verification

# %% Description
"""
Intro Exercise: Simple Calculator

Zaimplementuj dwie proste funkcje, żeby sprawdzić, że środowisko działa.
"""

# %% Hints
# - Funkcja add() powinna zwrócić sumę dwóch liczb
# - Funkcja multiply() powinna zwrócić iloczyn dwóch liczb

# %% Run
# - Terminal: `python -m doctest -f -v starter.py`
# - Tests: `python -m pytest test_hello.py -v`


def add(a, b):
    """
    Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b
