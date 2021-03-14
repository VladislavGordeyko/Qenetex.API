from sqlalchemy.orm import Session
from . import models, schemas


def get_address(db: Session, address_id: str):
    return db.query(models.Address).filter(models.Address.id == address_id).first()


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def get_addresses_ids(db: Session):
    return db.query(models.Address.id).all()


def create_address(db: Session, address: schemas.AddressCreate, generated_id: str):
    db_user = models.Address(id=generated_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_transaction(db: Session, transaction_id: str):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def get_transactions_by_address(db: Session, address_id: str):
    return db.query(models.Transaction).filter((models.Transaction.addr_to_id == address_id) |
                                               (models.Transaction.addr_from_id == address_id)).all()


def create_transaction(db: Session, item: schemas.TransactionCreate):
    db_item = models.Transaction(id=item.id, value=item.value, addr_to_id=item.addr_to_id,
                                 addr_from_id=item.addr_from_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
