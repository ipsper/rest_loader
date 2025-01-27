import requests

#BASE_URL = "http://192.168.1.102:8000"

def test_add_produkt(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "prodname": "Test Product",
        "productid": 1,
        "instock": 100,
        "prize": 9.99
    }
    response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "message" in data
    assert data["message"] == "Produkt added successfully"
    assert "produkt" in data
    assert data["produkt"]["prodname"] == "Test Product"

def test_read_stock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/stock/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "stock" in data

def test_delete_produkt(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # First, add a product to delete
    payload = {
        "prodname": "Test Product",
        "productid": 2,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code == 200
    productid = add_response.json()["produkt"]["productid"]

    # Now, delete the product
    delete_response = requests.delete(f"{BASE_URL}/stock/{productid}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Produkt deleted successfully"}

def test_decrease_stock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # First, add a product to decrease stock
    payload = {
        "prodname": "Test Product",
        "productid": 3,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code == 200
    productid = add_response.json()["produkt"]["productid"]

    # Now, decrease the stock
    decrease_payload = {
        "productid": productid,
        "amount": 10
    }
    decrease_response = requests.post(f"{BASE_URL}/stock/decrease/", json=decrease_payload)
    assert decrease_response.status_code == 200
    data = decrease_response.json()
    assert "message" in data
    assert data["message"] == "Decreased stock successfully"
    assert "new_stock" in data
    assert data["new_stock"] == 90

def test_increase_stock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # First, add a product to increase stock
    payload = {
        "prodname": "Test Product",
        "productid": 4,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code == 200
    productid = add_response.json()["produkt"]["productid"]

    # Now, increase the stock
    increase_payload = {
        "productid": productid,
        "amount": 10
    }
    increase_response = requests.post(f"{BASE_URL}/stock/increase/", json=increase_payload)
    assert increase_response.status_code == 200
    data = increase_response.json()
    assert "message" in data
    assert data["message"] == "Increased stock successfully"
    assert "new_stock" in data
    assert data["new_stock"] == 110

def test_change_price(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # First, add a product to change price
    payload = {
        "prodname": "Test Product",
        "productid": 5,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code == 200
    productid = add_response.json()["produkt"]["productid"]

    # Now, change the price
    change_price_payload = {
        "productid": productid,
        "new_price": 19.99
    }
    change_price_response = requests.post(f"{BASE_URL}/stock/change_price/", json=change_price_payload)
    assert change_price_response.status_code == 200
    data = change_price_response.json()
    assert "message" in data
    assert data["message"] == "Changed price successfully"
    assert "new_price" in data
    assert data["new_price"] == 19.99