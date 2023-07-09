import pytest
from market_microservice.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_all_market_summaries(client):
    response = client.get("/markets/summaries")
    assert response.status_code == 200


def test_get_market_summary(client):
    response = client.get("/markets?market=ltc-btc")
    assert response.status_code == 200


def test_get_market_summary_missing_param(client):
    response = client.get("/markets")
    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main()
