# Hur sättter man upp och använder pytest

[manual](https://docs.pytest.org/en/stable/)

1. konfigurera

```
cd $HOME/repo/rest_loader/pytesta
python3 -m venv pytesta_venv
source pytesta_venv/bin/activate
python -m pip install -r requirements.txt
```

2. test exemple

```
pytest tests/test_database.py

```

3. använd argument till start kommandot

uppdatera tests/conftest.py

- exemple

```
pytest tests/test_database.py --server_ip "127.0.0.1" --server_port "8000"

```

4. pytest.ini
   [dokumentation](pytest.ini)

här ligger tests/pytest.ini
