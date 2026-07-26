from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="Proration Calculator API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProrationRequest(BaseModel):
    old_price: float
    new_price: float
    days_remaining: float
    days_in_actual_month: float
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
        charge = price_difference * (
            request.days_remaining / 30.0
        )
    else:
        charge = price_difference * (
            request.days_remaining / request.days_in_actual_month
        )

    return {"charge": charge}