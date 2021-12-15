from babel import Locale
from figure_hook.Models import Webhook
from flask import Blueprint, current_app, flash, redirect, request
from flask.helpers import url_for
from flask_babel import force_locale, gettext

from hook_web.entities.session import DiscordAuthSession

from ..libs.discord_api import DiscordApi
from ..libs.tasks import send_notification_hook

blueprint = Blueprint("auth", __name__)
# logger = current_app.logger

"""Webhook Token Response Example
{
  "token_type": "Bearer",
  "access_token": "GNaVzEtATqdh173tNHEXY9ZYAuhiYxvy",
  "scope": "webhook.incoming",
  "expires_in": 604800,
  "refresh_token": "PvPL7ELyMDc1836457XCDh1Y8jPbRm",
  "webhook": {
    "application_id": "310954232226357250",
    "name": "testwebhook",
    "url": "https://discord.com/api/webhooks/347114750880120863/kKDdjXa1g9tKNs0-_yOwLyALC9gydEWP6gr9sHabuK1vuofjhQDDnlOclJeRIvYK-pj_",
    "channel_id": "345626669224982402",
    "token": "kKDdjXa1g9tKNs0-_yOwLyALC9gydEWP6gr9sHabuK1vuofjhQDDnlOclJeRIvYK-pj_",
    "type": 1,
    "avatar": null,
    "guild_id": "290926792226357250",
    "id": "347114750880120863"
  }
}
"""


@blueprint.route("/webhook", methods=["GET"])
def webhook():
    logger = current_app.logger
    request_args = request.args.to_dict()
    redirect_uri = url_for('public.home')

    if "error" in request_args:
        return redirect(url_for("public.home"))

    token_exchange_code = request_args.get('code')
    if token_exchange_code:
        auth_session = DiscordAuthSession()
        redirect_uri = url_for("auth.webhook", _external=True, _scheme='https')
        state = request_args["state"]
        token_response = DiscordApi.exchange_token(
            token_exchange_code,
            redirect_uri
        )

        state_is_valid = auth_session.is_state_valid(state)
        if token_response.status_code == 200 and state_is_valid:
            webhook_response = token_response.json()
            webhook_channel_id = webhook_response['webhook']['channel_id']
            webhook_id = webhook_response['webhook']["id"]
            webhook_token = webhook_response['webhook']['token']

            # TODO: if webhook_setting was lost, deal with it
            webhook_setting = auth_session.webhook_setting
            if webhook_setting:
                the_hook = save_webhook_info(
                    webhook_channel_id,
                    webhook_id,
                    webhook_token,
                    **webhook_setting
                )

                logger.info(f"${the_hook.id} created.")

                with force_locale(Locale.parse(webhook_setting.get('lang'), sep='-')):
                    welcome_msg = gettext("FigureHook hooked on this channel.")

                send_notification_hook(webhook_id, webhook_token, welcome_msg)
                flash(gettext("Hooking success!"), 'success')
            else:
                logger.error(f"Webhook settings in session is missing.")
                flash(gettext("Internal error. Please try again."), 'danger')

        elif token_response.status_code >= 400:
            error = token_response.json()
            if 'code' in error:
                if error['code'] == 30007:
                    flash(error['message'], 'danger')
            flash(gettext("Webhook authorization failed."), 'warning')

        redirect_uri = auth_session.entry_uri or url_for('public.home')
    return redirect(redirect_uri)


def save_webhook_info(channel_id, _id, token, **kwargs):
    the_hook = Webhook.get_by_channel_id(channel_id)
    if the_hook:
        the_hook.update(id=_id, token=token, **kwargs)
    if not the_hook:
        the_hook = Webhook.create(
            channel_id=channel_id, id=_id, token=token, **kwargs)
    the_hook.session.commit()
    return the_hook
