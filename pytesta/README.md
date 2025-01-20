# Hur sättter man upp och använder pytest

[manual](https://docs.pytest.org/en/stable/)

1. konfigurera

´´´
cd $HOME/repo/rest_loader/pytesta
python3 -m venv pytesta_venv
source pytesta_venv/bin/activate
python -m pip install -r requirements.txt
´´´

2. test exemple

´´´
pytest tests/test_database.py

´´´
