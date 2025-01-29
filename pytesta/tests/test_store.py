import requests

def test_first_read_stock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    response = requests.get(f"{BASE_URL}/stock/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "stock" in data

def test_add_produkt(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "prodname": "Test Product 1",
        "productid": 1,
        "instock": 100,
        "prize": 9.99
    }
    response = requests.post(f"{BASE_URL}/stock/", json=payload)
    if response.status_code == 400:
        data = response.json()
        print("test_add_produkt 400", data)
        assert response.status_code == 400
        assert "detail" in data
        detail = data["detail"]
        if isinstance(detail, str):
            assert "Product already exists" in detail
        else:
            assert detail["message"] == "Product already exists"
    if response.status_code == 200:
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        print("test_add_produkt 200", data)
        assert "message" in data
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
        "prodname": "Test Product 2",
        "productid": 2,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code == 200
    productid = add_response.json()["produkt"]["productid"]
    print("test_delete_produkt ", productid)
    # Now, delete the product
    delete_response = requests.delete(f"{BASE_URL}/stock/{productid}")
    back = delete_response.json()
    print("test_delete_produkt back", back)
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
    assert add_response.status_code in (200, 400)
    data = add_response.json()
    print("test_decrease_stock add_response:", data)
    if add_response.status_code == 400:
        assert "detail" in data
        detail = data["detail"]
        if isinstance(detail, str):
            assert "Product already exists" in detail
        else:
            assert detail["message"] == "Product already exists"
        # Fetch the productid since it already exists
        productid = payload["productid"]
    if add_response.status_code == 200:
        productid = data["produkt"]["productid"]
    in_stock = requests.get(f"{BASE_URL}/stock/{productid}/instock")
    print("test_decrease_stock in_stock:", in_stock)
    in_stock_data = in_stock.json()
    instocken = in_stock_data["instock"]
    print("test_decrease_stock instocken:", instocken)
    print("test_decrease_stock productid:", productid)
    reduse_with = 10
    # Now, decrease the stock
    decrease_payload = {
        "productid": productid,
        "amount": reduse_with
    }
    decrease_response = requests.post(f"{BASE_URL}/stock/decrease/", json=decrease_payload)
    print("test_decrease_stock decrease_response:", decrease_response)
    assert decrease_response.status_code == 200
    data = decrease_response.json()
    print("test_decrease_stock decrease_response:", data)
    assert "message" in data
    assert data["message"] == "Decreased stock successfully"
    assert "new_stock" in data
    assert data["new_stock"] == instocken - reduse_with

def test_increase_stock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    # First, add a product to increase stock
    payload = {
        "prodname": "Test Product 4",
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
        "prodname": "Test Product 5",
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


def test_get_instock(server_ip, server_port):
    BASE_URL = f"http://{server_ip}:{server_port}"
    productid = 1
    response = requests.get(f"{BASE_URL}/stock/{productid}/instock")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    print("test_get_instock response:", data)
    assert isinstance(data, dict)
    assert "productid" in data
    assert "instock" in data
    assert data["productid"] == productid
    assert isinstance(data["instock"], int)   