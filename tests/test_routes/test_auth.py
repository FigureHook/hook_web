from flask import url_for
from pytest_mock import MockerFixture


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


class FailedMockAuthReponse(MockAuthReponse):
    status = 400


class TestWebhookAuth:

    def test_successful_webhook_auth(self, client, mocker: MockerFixture):
        from hook_web.libs.discord_api import DiscordApi
        mocker.patch.object(DiscordApi, 'exchange_token',
                            return_value=MockAuthReponse())
        mocker.patch('hook_web.controllers.auth.save_webhook_info',
                     return_value=True)
        mocker.patch('hook_web.controllers.auth.check_state',
                     return_value=True)
        hook_sending = mocker.patch(
            'hook_web.controllers.auth.send_notification_hook')

        with client.session_transaction() as session:
            session['webhook_setting'] = {'lang': 'zh-TW'}
            session['entry_uri'] = '/'

        r = client.get(
            url_for('auth.webhook'),
            query_string={'code': "davidism",
                          'guild_id': "123", 'state': "123"},
            follow_redirects=True
        )

        assert r.status_code == 200
        assert b'message is-success' in r.data
        assert hook_sending.call_count == 1

        def test_faile_webhook_auth(self, client, mocker: MockerFixture):
            from hook_web.libs.discord_api import DiscordApi
            mocker.patch.object(DiscordApi, 'exchange_token',
                                return_value=FailedMockAuthReponse())
            saving_webhook = mocker.patch('hook_web.controllers.auth.save_webhook_info',
                                          return_value=True)
            mocker.patch('hook_web.controllers.auth.check_state',
                         return_value=True)
            hook_sending = mocker.patch(
                'hook_web.controllers.auth.send_notification_hook')

            with client.session_transaction() as session:
                session['webhook_setting'] = {'lang': 'zh-TW'}
                session['entry_uri'] = '/'

            r = client.get(
                url_for('auth.webhook'),
                query_string={'code': "davidism",
                              'guild_id': "123", 'state': "123"},
                follow_redirects=True
            )

            assert r.status_code == 400
            assert b'message is-warning' in r.data
            assert not hook_sending.called
            assert not saving_webhook.called
