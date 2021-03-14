import datetime
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Transaction model
class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(String, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now())
    value = Column(Float)

    addr_to_id = Column(String, ForeignKey("address.id"))
    addr_from_id = Column(String, ForeignKey("address.id"))

    addr_to = relationship("Address", foreign_keys=[addr_to_id], back_populates='transactions_to')
    addr_from = relationship("Address", foreign_keys=[addr_from_id], back_populates='transactions_from')


# Address model
class Address(Base):
    __tablename__ = "address"

    id = Column(String, primary_key=True)

    transactions_to = relationship("Transaction", foreign_keys='Transaction.addr_to_id', back_populates="addr_to")
    transactions_from = relationship("Transaction", foreign_keys='Transaction.addr_from_id', back_populates="addr_from")

