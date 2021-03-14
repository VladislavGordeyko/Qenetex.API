from typing import List
from pydantic import BaseModel
import datetime


class AddressTransactionCreate(BaseModel):
    address_id: str


class TransactionCreate(BaseModel):
    id: str
    value: float
    addr_to_id: str
    addr_from_id: str


class Transaction(BaseModel):
    id: str
    value: float
    date: datetime.datetime
    addr_to_id: str
    addr_from_id: str

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    pass


class AddressTransactions(BaseModel):
    id: str
    value: int

    class Config:
        orm_mode = True


class Address(BaseModel):
    id: str
    transactions_to: List[AddressTransactions] = []
    transactions_from: List[AddressTransactions] = []

    class Config:
        orm_mode = True
