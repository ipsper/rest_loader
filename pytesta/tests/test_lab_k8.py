import pytest
import requests
import time


def test_ips_are_up(ips, server_port):
    for ip in ips:
        url = f"http://{ip}:{server_port}/users/"
        try:
            response = requests.get(url, timeout=5)
            assert response.status_code == 200, f"IP {ip} is not up. Status code: {response.status_code}"
        except requests.RequestException as e:
            pytest.fail(f"IP {ip} is not reachable. Error: {e}")

def test_call_url_50_times(ips, server_port):
    results = []
    start_time = time.time()
    for _ in range(50):  # Gör 100 anrop totalt
        for ipa in ips:
            BASE_URL = f"http://{ipa}:{server_port}"
            response = requests.get(f"{BASE_URL}/users/")
            results.append(response.status_code)
            assert response.status_code == 200  # Kontrollera att statuskoden är 200
    end_time = time.time()
    duration = end_time - start_time
    print(f"Called URL 100 times in {duration:.2f} seconds")

    # Kontrollera att alla anrop returnerade statuskod 200
    assert all(status == 200 for status in results), "Not all requests returned status code 200"

def test_call_url_x_times(ips, server_port, amount):
    results = []
    start_time = time.time()
    for _ in range(amount):  
        for ipa in ips:
            BASE_URL = f"http://{ipa}:{server_port}"
            response = requests.get(f"{BASE_URL}/users/")
            results.append(response.status_code)
            assert response.status_code == 200  # Kontrollera att statuskoden är 200
    end_time = time.time()
    duration = end_time - start_time
    print(f"Called URL 100 times in {duration:.2f} seconds")

    # Kontrollera att alla anrop returnerade statuskod 200
    assert all(status == 200 for status in results), "Not all requests returned status code 200"