# filepath: /home/per/repo/rest_loader/pytesta/tests/test_loader.py
import requests
import time

def test_process__chunks(server_ip, server_port, interval, amount):
    BASE_URL = f"http://{server_ip}:{server_port}"
    payload = {
        "chunk": {
            str(i): {
                "host": server_ip,
                "port": server_port,
                "metoderna": "GET",
                "endpoint": "/stock/",
                "body": None
            } for i in range(1, amount + 1)
        },
        "interval": interval
    }
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/process_chunks/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print("test_process_100_chunks data", data)
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
    print("test_process_100_chunks duration", duration)

    # Print status code statistics
    print("Status code statistics:")
    for status_code, count in data["status_code_statistics"].items():
        print(f"Status code {status_code}: {count} times")

    # Convert status_code_statistics keys to integers for comparison
    status_code_statistics = {int(k): v for k, v in data["status_code_statistics"].items()}

    # Compare the number of 200 status codes with the amount
    assert status_code_statistics.get(200, 0) == amount, (
        f"Expected {amount} status code 200 responses, but got {status_code_statistics.get(200, 0)}"
    )