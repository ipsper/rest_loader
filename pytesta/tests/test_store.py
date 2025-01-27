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
    get_all_response = requests.get(f"{BASE_URL}/stock/productids/")
    print("get all productids 200", get_all_response.json())


    payload = {
        "prodname": "Test Product 3",
        "productid": 3,
        "instock": 100,
        "prize": 9.99
    }
    add_response = requests.post(f"{BASE_URL}/stock/", json=payload)
    assert add_response.status_code in (200, 400)
    if add_response.status_code == 400:
        data = add_response.json()
        assert "detail" in data
        detail = data["detail"]
        if isinstance(detail, str):
            assert "Product already exists" in detail
        else:
            assert detail["message"] == "Product already exists"
    if add_response.status_code == 200:
        print("test_decrease_stock 200",)
    print("test_decrease_stock ", add_response.json())
    productid = add_response.json()["produkt"]["productid"]
    print("test_decrease_stock back", productid)

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