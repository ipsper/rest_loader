(rest_loader_venv) per@per-PN52:~/repo/rest_loader$ uvicorn app.main:app --reload
INFO: Will watch for changes in these directories: ['/home/per/repo/rest_loader']
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process [81583] using StatReload
Python version: 3.12.3 (main, Jan 17 2025, 18:03:48) [GCC 13.3.0]
Process SpawnProcess-1:
Traceback (most recent call last):
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 941, in do_execute
cursor.execute(statement, parameters)
psycopg2.errors.InsufficientPrivilege: permission denied for schema public
LINE 2: CREATE TABLE cards (
^

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
File "/usr/lib/python3.12/multiprocessing/process.py", line 314, in \_bootstrap
self.run()
File "/usr/lib/python3.12/multiprocessing/process.py", line 108, in run
self.\_target(\*self.\_args, **self.\_kwargs)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/\_subprocess.py", line 80, in subprocess_started
target(sockets=sockets)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/server.py", line 65, in run
return asyncio.run(self.serve(sockets=sockets))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
return runner.run(main)
^^^^^^^^^^^^^^^^
File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
return self.\_loop.run_until_complete(task)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.12/asyncio/base_events.py", line 687, in run_until_complete
return future.result()
^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/server.py", line 69, in serve
await self.\_serve(sockets)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/server.py", line 76, in \_serve
config.load()
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/config.py", line 434, in load
self.loaded_app = import_from_string(self.app)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/uvicorn/importer.py", line 19, in import_from_string
module = importlib.import_module(module_str)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.12/importlib/**init**.py", line 90, in import_module
return \_bootstrap.\_gcd_import(name[level:], package, level)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "<frozen importlib._bootstrap>", line 1387, in \_gcd_import
File "<frozen importlib._bootstrap>", line 1360, in \_find_and_load
File "<frozen importlib._bootstrap>", line 1331, in \_find_and_load_unlocked
File "<frozen importlib._bootstrap>", line 935, in \_load_unlocked
File "<frozen importlib._bootstrap_external>", line 995, in exec_module
File "<frozen importlib._bootstrap>", line 488, in \_call_with_frames_removed
File "/home/per/repo/rest_loader/app/main.py", line 7, in <module>
from .routes_cards import router as cards_router # Import the cards router
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/app/routes_cards.py", line 23, in <module>
Base.metadata.create_all(bind=engine)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/schema.py", line 5868, in create_all
bind.\_run_ddl_visitor(
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 3253, in \_run_ddl_visitor
conn.\_run_ddl_visitor(visitorcallable, element, **kwargs)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2459, in \_run_ddl_visitor
visitorcallable(self.dialect, self, **kwargs).traverse_single(element)
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/visitors.py", line 664, in traverse_single
return meth(obj, **kw)
^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 918, in visit_metadata
self.traverse_single(
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/visitors.py", line 664, in traverse_single
return meth(obj, \*\*kw)
^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 956, in visit_table
).\_invoke_with(self.connection)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 314, in \_invoke_with
return bind.execute(self)
^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1418, in execute
return meth(
^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/sql/ddl.py", line 180, in \_execute_on_connection
return connection.\_execute_ddl(
^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1529, in \_execute_ddl
ret = self.\_execute_context(
^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1846, in \_execute_context
return self.\_exec_single_context(
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1986, in \_exec_single_context
self.\_handle_dbapi_exception(
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2355, in \_handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1967, in \_exec_single_context
self.dialect.do_execute(
File "/home/per/repo/rest_loader/rest_loader_venv/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 941, in do_execute
cursor.execute(statement, parameters)
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.InsufficientPrivilege) permission denied for schema public
LINE 2: CREATE TABLE cards (
^

[SQL:
CREATE TABLE cards (
id SERIAL NOT NULL,
created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
title VARCHAR NOT NULL,
description VARCHAR,
PRIMARY KEY (id)
)

]
(Background on this error at: https://sqlalche.me/e/20/f405)
