from typing import Optional

from flask import session


class DiscordAuthSession:
    def __init__(self) -> None:
        self._session = session

    @property
    def state(self) -> Optional[str]:
        return self._session.get('state')

    @state.setter
    def state(self, value: str):
        self._session.setdefault('state', value)

    @property
    def entry_uri(self) -> Optional[str]:
        return self._session.get('entry_uri')

    @entry_uri.setter
    def entry_uri(self, uri: str):
        self._session.setdefault('entry_uri', uri)

    @property
    def webhook_setting(self) -> Optional[dict]:
        return self._session.get('webhook_setting')

    @webhook_setting.setter
    def webhook_setting(self, setting: dict):
        self._session.setdefault('webhook_setting', setting)

    def is_state_valid(self, outside_state: str) -> bool:
        return self.state != outside_state
