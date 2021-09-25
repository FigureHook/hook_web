from flask.helpers import url_for

from hook_web.entities.session import DiscordAuthSession


class TestDiscordAuthSession:
    def test_attributes(self, client):
        client.get("/")
        auth_session = DiscordAuthSession()

        assert hasattr(auth_session, 'state')
        assert hasattr(auth_session, 'webhook_setting')
        assert hasattr(auth_session, 'entry_uri')

    def test_get_session(self, client):
        with client.session_transaction() as session:
            session['state'] = "kappa"
            session['entry_uri'] = "uri"
            session['webhook_setting'] = "webhook_setting"

        client.get("/")
        auth_session = DiscordAuthSession()
        assert auth_session.state
        assert auth_session.entry_uri
        assert auth_session.webhook_setting

    def test_set_session(self, client):
        client.get("/")
        auth_session = DiscordAuthSession()

        auth_session.state = "kappa"
        auth_session.webhook_setting = {
            'is_nsfw': True,
            'lang': "zh-TW"
        }
        auth_session.entry_uri = url_for('public.home')

        assert auth_session.state
        assert auth_session.entry_uri
        assert auth_session.webhook_setting
