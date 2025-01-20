import pytest
import httpx
import requests

BASE_URL = "http://192.168.1.102:8000"

def test_read_users():
        BASE_URL = "http://192.168.1.102:8000"
        response =  requests.get(f"{BASE_URL}/users/")
        print("returen code", response.status_code)
        assert response.status_code == 200
        print("returen", response.json())
        assert response.headers["content-type"] == "application/json"
        assert isinstance(response.json(), dict)  # Assuming the response is a JSON object