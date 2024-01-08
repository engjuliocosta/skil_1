from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_accounts_payable():
    """Must list accounts payable."""
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
    account = {
        "description": "casa",
        "value": 600,
        "account_type": "essential"
    }
    response = client.post("/accounts_payable", json=account)
    assert response.status_code == 201
