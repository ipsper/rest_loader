# divers om pytest

## patametrar

- alla parametrar kommer grån kommer från conftest.py
  --server_ip
  --server_port

## Kommandon

pytest -s tests/test_cards.py --server_ip "127.0.0.1" --server_port "8000"

pytest -svvx tests/test_loader.py --server_ip "127.0.0.1" --server_port "8000" --interval "10" --amount 99

## pytest options förklaring

- hanterar output från testfall
  -s # disable all capturing
  --capture=sys # replace sys.stdout/stderr with in-mem files
  --capture=fd # also point filedescriptors 1 and 2 to temp file

- stanna vid fel/error i testfall
  -x # stop after first failure
  --maxfail=2 # stop after two failures

- kontrollera hur pratig
  -q # quiet - less verbose - mode (shortcut)
  -v # increase verbosity, display individual test names

- kör enbart ett testfall i en test_file.py
  test_file.py::test_function_name

## k8 lab tester

pytest -svvx tests/test_lab_k8.py --ips 192.168.1.101,192.168.1.102 --server_port "8000" --amount 99

pytest -svvx tests/test_loader.py --load_ip "127.0.0.1" --load_port "8000" --ips 192.168.1.101,192.168.1.102 --server_port "8000" --amount 1000 --per_second 100 --per_minute None

pytest -svvx tests/test_loader.py --load_ip "127.0.0.1" --load_port "8000" --ips 192.168.1.101,192.168.1.102 --server_port "8000" --amount 1000 --per_second 100 --per_minute None

pytest -svvx tests/test_loader.py --load_ip "127.0.0.1" --load_port "8000" --ips "192.168.1.101,192.168.1.102" --server_port "8000" --per_second 100 --amount 1000

pytest -svvx tests/test_loader.py --load_ip "127.0.0.1" --load_port "8000" --ips 192.168.1.101,192.168.1.102 --server_port "8000" --amount 1000 --per_second 100

pytest -svvx tests/test_loader.py --load_ip "127.0.0.1" --load_port "8000" --ips 192.168.1.101,192.168.1.102 --server_port "8000" --amount 100 --per_second 0 --per_minute 10

# debugging

curl -X 'POST' \
 'http://127.0.0.1:8000/process_chunks/?workers=10' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"chunk": {
"additionalProp1": {
"host": "192.168.1.101",
"port": "8000",
"metoderna": "GET",
"endpoint": "/users/",
"body": "None"
},
"additionalProp2": {
"host": "192.168.1.102",
"port": "8000",
"metoderna": "GET",
"endpoint": "/users/",
"body": "None"
},
"additionalProp3": {
"host": "192.168.1.101",
"port": "8000",
"metoderna": "GET",
"endpoint": "/users/",
"body": "None"
}
},
"requests_per_second": 10,
"requests_per_minute": 600
}'

{'chunk': {'1': {'host': '192.168.1.101', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '2': {'host': '192.168.1.102', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '3': {'host': '192.168.1.101', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '4': {'host': '192.168.1.102', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '5': {'host': '192.168.1.101', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '6': {'host': '192.168.1.102', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '7': {'host': '192.168.1.101', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '8': {'host': '192.168.1.102', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '9': {'host': '192.168.1.101', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}, '10': {'host': '192.168.1.102', 'port': '8000', 'metoderna': 'GET', 'endpoint': '/users/', 'body': 'None'}}, 'requests_per_second': '100', 'requests_per_minute': 'None'}
