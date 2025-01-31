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

##
