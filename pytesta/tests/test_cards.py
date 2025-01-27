import requests

#BASE_URL = "http://192.168.1.102:8000"


def test_read_cards(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/cards/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "cards" in data

def test_create_card(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    print("test_create_card BASE_URL", BASE_URL)
    payload = {
        "cardnumber": "88888888888",
        "month_year": "88",
        "cvc": "555",
        "cardholder": "Pelle Plutt"
    }
    response = requests.post(f"{BASE_URL}/cards/", json=payload)
    print("test_create_card returen code", response.status_code)
    assert response.status_code == 200
    print("test_create_card returen", response.json())
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), dict)

def test_delete_card(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # Create a card to delete
    payload = {
        "cardnumber": "88888888888",
        "month_year": "88",
        "cvc": "555",
        "cardholder": "Pelle Plutt"
    }
    create_response = requests.post(f"{BASE_URL}/cards/", json=payload)
    assert create_response.status_code == 200
    card_id = create_response.json()["card"]["id"]

    # Delete the card
    delete_response = requests.delete(f"{BASE_URL}/cards/{card_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Card deleted successfully"}

def test_count_cards(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    print("test_count_cards BASE_URL", BASE_URL)
    response = requests.get(f"{BASE_URL}/cards/count/")
    print("test_count_cards returen code", response.status_code)
    assert response.status_code == 200
    print("test_count_cards returen", response.json())
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(response.json(), dict)
    assert "count" in data
    print("Number of cards:", data["count"])
    assert data["count"] > 0

def test_count_unique_cardholders(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/cards/cardholders/count/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "count" in data

def test_count_cardholder(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "cardholder": "Pelle Plutt"
    }
    response = requests.post(f"{BASE_URL}/cards/cardholder/count/", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "cardholder" in data
    assert "count" in data

def test_list_cardholders(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/cards/cardholders/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "cardholders" in data
    assert isinstance(data["cardholders"], list)

def test_get_card_by_id(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # Create a card to retrieve
    payload = {
        "cardnumber": "88888888888",
        "month_year": "88",
        "cvc": "555",
        "cardholder": "Pelle Plutt"
    }
    create_response = requests.post(f"{BASE_URL}/cards/", json=payload)
    assert create_response.status_code == 200
    card_id = create_response.json()["card"]["id"]

    # Retrieve the card by id
    response = requests.get(f"{BASE_URL}/cards/{card_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == card_id