# filepath: /home/per/repo/rest_loader/pytesta/tests/test_loader.py
import requests
import time

def test_process_chunks(server_ip, server_port, interval):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "chunk": {
            "1": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            },
            "2": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            },
            "3": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            },
            "4": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            },
             "5": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            },
            "6": {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            }             
        },
        "interval": interval  # Konfigurerbart intervall i mikrosekunder # Konfigurerbart intervall
    }
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/process_chunks/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print("test_process_chunks data", data)
    for result in data["results"]:
        assert "chunk_id" in result
        assert "result" in result
        assert "status_code" in result["result"]
        assert "duration" in result["result"]
        if "error" in result["result"]:
            assert isinstance(result["result"]["error"], str)
        else:
            assert "response" in result["result"]
    end_time = time.time()
    duration = end_time - start_time
    lenduration = len(payload["chunk"])
    print("test_process_chunks interval", interval)
    print("test_process_chunks len chunk", lenduration)
    print("test_process_chunks duration", interval * duration)
    assert duration > interval * lenduration
