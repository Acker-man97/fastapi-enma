import pytest
from app.calculations import add,subtract,multiply,divide

@pytest.mark.parametrize("num1,num2,result", [
    (3,2,5), (8,9,17), (5,10,15), 
])
def test_add(num1,num2,result):
    print("Test Successful")
    assert add (num1 , num2) == result


@pytest.mark.parametrize("num1,num2,result", [
    (3,2,6), (8,9,72), (5,10,50), ])
def test_multiply(num1,num2,result):
    assert multiply (num1 , num2) == result