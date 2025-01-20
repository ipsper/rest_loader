import pytest
import httpx
import requests

#BASE_URL = "http://192.168.1.102:8000"

def test_read_users(server_ip, server_port):
        BASE_URL = f"http://{server_ip}:{server_port}"
        print("BASE_URL", BASE_URL)
#        BASE_URL = "http://192.168.1.102:8000"
        response =  requests.get(f"{BASE_URL}/users/")
        print("returen code", response.status_code)
        assert response.status_code == 200
        print("returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)  # Assuming the response is a JSON object