from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Form


app = FastAPI()
@app.get("/solve/{a}/{b}/{c}")
async def solve(a: float, b: float, c: float):
    solution = solve_quadratic_equation(a, b, c)
    match solution:
        case None:
            return {"number_of_solutions": 0}
        case (x_1, x_2):
            return {"number_of_solutions": 2, "x_1": x_1, "x_2": x_2}
        case x:
            return {"number_of_solutions": 1, "x": x}