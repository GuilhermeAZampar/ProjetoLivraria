import pytest

def somar(a,b):
    return a+b

def test_somar():
    resultado=somar(2,3)
    assert resultado == 5


