from pydantic import BaseModel, Field

from typing import List

class RunCodeActionScheme(BaseModel):
    code: str = Field(
        description='The code to retrieve the execution result',
        min_length=1,
        max_length=2056,
        default='def test_function(a: int, b: int) -> int:\n    return a + b\n\nprint(test_function(10, 20)) # 30'
    )

class ToVectorsActionScheme(BaseModel):
    code1: str = Field(
        description='The first version of the code or the result of the execution',
        min_length=1,
        max_length=2056,
        default='def test_function(a: int, b: int) -> int: return a + b print(test_function(10, 20)) # 30'
    )
    code2: str = Field(
        description='The second version of the code or the result of the execution',
        min_length=1,
        max_length=2056,
        default='def my_func(a: float, b: float) -> str: return a + b print(my_func(10, 20)) # 30'
    )

class CompareVectorsActionScheme(BaseModel):
    vector1: List[float] = Field(
        description='The vector of the first code or the result of the execution',
        default=[
            0.1776691754583681,
            0.1776691754583681,
            0.1776691754583681,
            0.1776691754583681,
            0,
            0.7491234806792513,
            0,
            0.1776691754583681,
            0.1776691754583681,
            0,
            0.49941565378616753
        ]
    )
    vector2: List[float] = Field(
        description='The vector of the second code or the result of the execution',
        default=[
            0.20507486496143149,
            0.20507486496143149,
            0.20507486496143149,
            0.20507486496143149,
            0.576451134506571,
            0,
            0.576451134506571,
            0.20507486496143149,
            0.20507486496143149,
            0.2882255672532855,
            0
        ]
    )