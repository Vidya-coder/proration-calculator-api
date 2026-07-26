from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(title="Proration Calculator API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProrationRequest(BaseModel):
    old_price: float = Field(ge=0)
    new_price: float = Field(ge=0)
    days_remaining: int = Field(ge=0)
    days_in_actual_month: int = Field(ge=1, le=31)
    spec: Literal["v1", "v2"]


class ProrationResponse(BaseModel):
    charge: float


@app.get("/")
def root():
    return {"message": "Proration Calculator API is running"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/charge", response_model=ProrationResponse)
def calculate_charge(request: ProrationRequest):
    price_difference = request.new_price - request.old_price

    if request.spec == "v1":
        divisor = 30
    else:
        divisor = request.days_in_actual_month

    charge = price_difference * (request.days_remaining / divisor)

    return {"charge": charge}