import requests

#BASE_URL = "http://192.168.1.102:8000"


def test_read_users(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/users/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "users" in data

def test_create_user(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    print("test_create_card BASE_URL", BASE_URL)
    payload = {
        "name": "string",
        "email": "string",
        "street": "string",
        "street_number": "string",
        "city": "string",
        "zip": "string",
        "country": "string"
    }
    response = requests.post(f"{BASE_URL}/users/", json=payload)
    print("test_create_user returen code", response.status_code)
    assert response.status_code == 200
    print("test_create_card returen", response.json())
    assert response.headers["content-type"] == "application/json"
    assert isinstance(response.json(), dict)

def test_delete_user(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # Create a card to delete
    payload = {
        "name": "string",
        "email": "string",
        "street": "string",
        "street_number": "string",
        "city": "string",
        "zip": "string",
        "country": "string"
    }
    create_response = requests.post(f"{BASE_URL}/users/", json=payload)
    assert create_response.status_code == 200
    card_id = create_response.json()["name"]["id"]

    # Delete the card
    delete_response = requests.delete(f"{BASE_URL}/users/{card_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted successfully"}

def test_count_users(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    print("test_count_users BASE_URL", BASE_URL)
    response = requests.get(f"{BASE_URL}/users/count/")
    print("test_count_users returen code", response.status_code)
    assert response.status_code == 200
    print("test_count_users returen", response.json())
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(response.json(), dict)
    assert "count" in data
    print("Number of users:", data["count"])
    assert data["count"] > 0

def test_count_unique_users(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/users/cardholders/count/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "count" in data

def test_count_cardholder(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "name": "Pelle Plutt"
    }
    response = requests.post(f"{BASE_URL}/users/cardholder/count/", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "cardholder" in data
    assert "count" in data

def test_list_cardholders(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/users/cardholders/")
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
        "name": "string",
        "email": "string",
        "street": "string",
        "street_number": "string",
        "city": "string",
        "zip": "string",
        "country": "string"
    }
    create_response = requests.post(f"{BASE_URL}/users/", json=payload)
    assert create_response.status_code == 200
    card_id = create_response.json()["card"]["id"]

    # Retrieve the card by id
    response = requests.get(f"{BASE_URL}/users/{card_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == card_id