import requests as rq
import os


class DiscordApi:
    __endpoint__ = "https://discord.com/api/v8"

    @classmethod
    def exchange_token(cls, exchange_code, redirect_uri):
        data = {
            "client_id": os.getenv("DISCORD_CLIENT_ID"),
            "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": exchange_code,
            "redirect_uri": redirect_uri
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        r = rq.post(f"{cls.__endpoint__}/oauth2/token",
                    data=data, headers=headers)
        return r
