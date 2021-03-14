
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import repository, models, schemas
from database.db import SessionLocal, engine
from utils import generate_hex, generate_float, pick_random_elements

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# add here address of frontend server to prevent cors error
origins = [
    "http://localhost:3000",
]

# Cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add address
@app.post("/address/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return repository.create_address(db=db, address=address, generated_id=generate_hex(8))


# Get address list
@app.get("/address/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = repository.get_addresses(db, skip=skip, limit=limit)
    return addresses


# Get address by id
@app.get("/address/{address_id}", response_model=schemas.Address)
def read_address(address_id: str, db: Session = Depends(get_db)):
    db_addr = repository.get_address(db, address_id=address_id)
    if db_addr is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_addr


# Get transaction by id
@app.get("/transaction/{transaction_id}", response_model=schemas.Address)
def read_address(transaction_id: str, db: Session = Depends(get_db)):
    db_transaction = repository.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


# Get Transactions list
@app.get("/transaction/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = repository.get_transactions(db, skip=skip, limit=limit)
    return items


# Get Transaction by address id
@app.get("/transaction/address/{address_id}", response_model=List[schemas.Transaction])
def read_transactions_by_address(address_id: str, db: Session = Depends(get_db)):
    items = repository.get_transactions_by_address(db, address_id)
    return items


# Add random transaction
@app.post("/transaction/")
def create_random_transaction(db: Session = Depends(get_db)):
    address_ids = [value for value, in repository.get_addresses_ids(db)]
    addresses = pick_random_elements(address_ids)

    new_transaction = schemas.TransactionCreate(id=generate_hex(16), value=generate_float(),
                                                addr_to_id=addresses[0], addr_from_id=addresses[1])
    return repository.create_transaction(db=db, item=new_transaction)


# Add transaction with address
@app.post("/address_transaction/",  response_model=schemas.Transaction)
def create_transaction(address: schemas.AddressTransactionCreate, db: Session = Depends(get_db)):
    address_ids = [value for value, in repository.get_addresses_ids(db)]
    addresses = pick_random_elements(address_ids, 1)

    new_transaction = schemas.TransactionCreate(id=generate_hex(16), value=generate_float(),
                                                addr_to_id=addresses[0], addr_from_id=address.address_id)
    return repository.create_transaction(db=db, item=new_transaction)
