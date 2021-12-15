import pytest


@pytest.fixture(scope='session')
def client():
    from figure_hook.database import PostgreSQLDB
    from figure_hook.Models.base import Model

    from hook_web.app import create_app

    app = create_app("test")
    pgsql = PostgreSQLDB()
    Model.metadata.create_all(pgsql.engine)

    with app.test_client() as client:
        with app.app_context():
            yield client

    Model.metadata.drop_all(pgsql.engine)
