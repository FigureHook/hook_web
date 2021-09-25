from babel import Locale
from figure_hook.Models import Webhook
from flask import Blueprint, flash, redirect, request, session
from flask.helpers import url_for
from flask_babel import force_locale, gettext

from hook_web.entities.session import DiscordAuthSession

from ..libs.discord_api import DiscordApi
from ..libs.tasks import send_notification_hook

blueprint = Blueprint("auth", __name__)


@blueprint.route("/webhook", methods=["GET"])
def webhook():
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
            token_exchange_code, redirect_uri
        )

        if token_response.status_code == 200 and auth_session.is_state_valid(state):
            webhook_response = token_response.json()
            webhook_channel_id = webhook_response['webhook']['channel_id']
            webhook_id = webhook_response['webhook']["id"]
            webhook_token = webhook_response['webhook']['token']

            # TODO: if webhook_setting was lost, deal with it
            webhook_setting = auth_session.webhook_setting
            if webhook_setting:
                save_webhook_info(webhook_channel_id, webhook_id,
                                  webhook_token, **webhook_setting)

                with force_locale(Locale.parse(webhook_setting.get('lang'), sep='-')):
                    msg = gettext("FigureHook hooked on this channel.")

                send_notification_hook(webhook_id, webhook_token, msg)
                flash(gettext("Hooking success!"), 'success')

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
