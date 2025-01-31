import pytest

def pytest_addoption(parser):
    parser.addoption("--name", action="store")
    parser.addoption("--user", action="store")
    parser.addoption("--username", action="store")
    parser.addoption("--dev_pw", action="store")
    parser.addoption("--node_nr", action="store")
    parser.addoption("--server", action="store")
    parser.addoption("--dbg", action="store")
    parser.addoption("--venv", action="store")
    parser.addoption("--devsuite", action="store")
    parser.addoption("--location", action="store")
    parser.addoption("--client", action="store")
    parser.addoption("--client_typ", action="store")
    parser.addoption("--interval", action="store", type=int, default="0", help="Interval/backpresure timeout for the tests")
    parser.addoption("--server_ip", action="store", default="127.0.0.1", help="Server IP for the tests")
    parser.addoption("--server_port", action="store", default="8000", help="Server port for the tests")
    parser.addoption("--amount", action="store", type=int, default="1", help="Bra att kunna speca antal för testerna")


@pytest.fixture(scope='session')
def name(request):
    name_value = request.config.option.name
    if name_value is None:
        pytest.skip()
    return name_value

@pytest.fixture(scope='session')
def user(request):
    user_value = request.config.option.user
    if user_value is None:
        pytest.skip()
    return user_value

@pytest.fixture(scope='session')
def username(request):
    username_value = request.config.option.username
    if username_value is None:
        pytest.skip()
    return username_value

@pytest.fixture(scope='session')
def dev_pw(request):
    dev_pw_value = request.config.option.dev_pw
    if dev_pw_value is None:
        pytest.skip()
    return dev_pw_value

@pytest.fixture(scope='session')
def node_nr(request):
    node_nr_value = request.config.option.node_nr
    if node_nr_value is None:
        pytest.skip()
    return node_nr_value

@pytest.fixture(scope='session')
def server(request):
    server_value = request.config.option.server
    if server_value is None:
        pytest.skip()
    return server_value

@pytest.fixture(scope='session')
def dbg(request):
    dbg_value = request.config.option.dbg
    if dbg_value is None:
        pytest.skip()
    return dbg_value

@pytest.fixture(scope='session')
def venv(request):
    venv_value = request.config.option.venv
    if venv_value is None:
        pytest.skip()
    return venv_value

@pytest.fixture(scope='session')
def devsuite(request):
    devsuite_value = request.config.option.devsuite
    if devsuite_value is None:
        pytest.skip()
    return devsuite_value

@pytest.fixture(scope='session')
def location(request):
    location_value = request.config.option.location
    if location_value is None:
        pytest.skip()
    return location_value

@pytest.fixture(scope='session')
def client(request):
    client_value = request.config.option.client
    if client_value is None:
        pytest.skip()
    return client_value

@pytest.fixture(scope='session')
def client_typ(request):
    client_typ_value = request.config.option.client_typ
    if client_typ_value is None:
        pytest.skip()
    return client_typ_value

@pytest.fixture(scope='session')
def server_ip(request):
    client_typ_value = request.config.option.server_ip
    if client_typ_value is None:
        pytest.skip()
    return client_typ_value

@pytest.fixture(scope='session')
def server_port(request):
    client_typ_value = request.config.option.server_port
    if client_typ_value is None:
        pytest.skip()
    return client_typ_value

@pytest.fixture(scope='session')
def interval(request):
    client_typ_value = request.config.option.interval
    if client_typ_value is None:
        pytest.skip()
    return client_typ_value

@pytest.fixture(scope='session')
def amount(request):
    client_typ_value = request.config.option.amount
    if client_typ_value is None:
        pytest.skip()
    return client_typ_value
