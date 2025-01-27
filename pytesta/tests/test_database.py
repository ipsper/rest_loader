import requests

#BASE_URL = "http://192.168.1.102:8000"

def test_read_users(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("test_read_users BASE_URL", BASE_URL)
        response =  requests.get(f"{BASE_URL}/users/")
        print("test_read_users returen code", response.status_code)
        assert response.status_code == 200
        print("test_read_users returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)

def test_read_cards(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("test_read_cards BASE_URL", BASE_URL)
        response =  requests.get(f"{BASE_URL}/cards/")
        print("test_read_cards returen code", response.status_code)
        assert response.status_code == 200
        print("test_read_cards returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)

def test_tables_cards(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("test_read_tables BASE_URL", BASE_URL)
        response =  requests.get(f"{BASE_URL}/tables/")
        print("test_read_tables returen code", response.status_code)
        assert response.status_code == 200
        print("test_read_tables returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)

def test_tables_stock(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("test_read_stock BASE_URL", BASE_URL)
        response =  requests.get(f"{BASE_URL}/stock/")
        print("test_read_stock returen code", response.status_code)
        assert response.status_code == 200
        print("test_read_stock returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)

def test_tables_purchase(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("test_tables_purchase BASE_URL", BASE_URL)
        response =  requests.get(f"{BASE_URL}/purchase/")
        print("test_tables_purchase returen code", response.status_code)
        assert response.status_code == 200
        print("test_tables_purchase returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)
