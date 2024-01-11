from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.dbhandler import Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_list_accounts_payable():
    """Must test list accounts payable."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/accounts_payable",
                json={"description": "casa",
                      "value": 600,
                      "account_type": "essential"})

    response = client.get("/accounts_payable")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1,
         "description": "casa",
         "value": 600,
         "account_type": "essential"}
    ]


def test_create_accounts_payable():
    """Must test create accounts payable."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "casa",
        "value": 600,
        "account_type": "essential"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 201


def test_return_error_when_exceed_description():
    """Must test return error when exceed description with 30 caracters."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "012345678901234567890123456789",
        "value": 600,
        "account_type": "essential"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "account_type"]


def test_return_error_when_description_is_less_than_3():
    """Must test return error when description is less than 3 caracters."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "12",
        "value": 600,
        "account_type": "essential"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 422


def test_return_error_account_type_is_less_than_3():
    """Must test return error when account type is less than 3 caracters."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "casa",
        "value": 600,
        "account_type": "es"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 422


def test_return_error_account_type_is_greater_than_30():
    """Must test return error when account type is greater than 30 caracters."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "casa",
        "value": 600,
        "account_type": "012345678901234567890123456789"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 422


def teste_return_error_when_value_is_zero():
    """Must test return error when value is zero."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    account = {
        "description": "casa",
        "value": -1,
        "account_type": "essential"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 422


def test_update_account_payable():
    """Must test update account."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/accounts_payable",
                           json={"description": "casa",
                                 "value": 600,
                                 "account_type": "essential"})

    id_account = response.json()["id"]

    client.put("/accounts_payable" / {id_account},
               json={"description": "casa",
                     "value": 111,
                     "account_type": "essential"})

    assert response.status_code == 200
