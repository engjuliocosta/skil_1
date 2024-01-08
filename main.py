from fastapi import FastAPI

from accounts_payable.routers import accounts_payable
from payment_receipts.routers import payment_receipts
from shared.dbhandler import Base, engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Primeira API": "API Pagamentos"}


app.include_router(accounts_payable.router)
app.include_router(payment_receipts.router)
