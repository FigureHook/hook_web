from flask import url_for
from pytest_mock import MockerFixture


def test_webhook_auth(client, mocker: MockerFixture):
    class MockAuthReponse:
        status = 200

        @property
        def status_code(self):
            return self.status

        def json(self):
            return {
                "webhook": {
                    "channel_id": "123",
                    "id": "564",
                    "token": "secret"
                }
            }

    from hook_web.libs.discord_api import DiscordApi
    mocker.patch.object(DiscordApi, 'exchange_token',
                        return_value=MockAuthReponse())
    mocker.patch('hook_web.controllers.auth.save_webhook_info',
                 return_value=True)
    mocker.patch('hook_web.controllers.auth.check_state', return_value=True)
    mocker.patch('hook_web.libs.tasks.send_notification_hook')

    with client.session_transaction() as session:
        session['webhook_setting'] = {'lang': 'zh-TW'}
        session['entry_uri'] = '/'

    r = client.get(
        url_for('auth.webhook'),
        query_string={'code': "davidism", 'guild_id': "123", 'state': "123"},
        follow_redirects=True
    )

    assert r.status_code == 200
    assert b'message is-success' in r.data

    MockAuthReponse.status = 400
    r = client.get(
        url_for('auth.webhook'),
        query_string={'code': "davidism", 'guild_id': "123", 'state': "123"},
        follow_redirects=True
    )

    assert r.status_code == 200
    assert b'message is-warning' in r.data
