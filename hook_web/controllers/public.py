import os
import urllib.parse
from base64 import urlsafe_b64encode

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_babel import get_locale, gettext

from ..forms import SubscriptionForm, locale_language_choice

blueprint = Blueprint("public", __name__)


def concate_discord_auth_uri_with_state(state):
    base_uri = "https://discord.com/api/oauth2/authorize?"
    redirect_uri = url_for('auth.webhook', _external=True, _scheme='https')
    client_id = os.getenv('DISCORD_CLIENT_ID')
    query_string = urllib.parse.urlencode(
        {
            'response_type': "code",
            'client_id': client_id,
            'scope': "webhook.incoming",
            'redirect_uri': redirect_uri,
            'state': state
        }
    )

    return f"{base_uri}{query_string}"


@blueprint.route("/", methods=('GET', 'POST'))  # type: ignore
def home():
    locale = get_locale()
    default_lang = locale_language_choice[str(locale)][0]
    form = SubscriptionForm(language=default_lang)

    if request.method == 'GET':
        return render_template("index.html", form=form, lang=str(locale))

    if request.method == 'POST':
        if form.validate_on_submit():
            session['entry_uri'] = request.path

            state = urlsafe_b64encode(os.urandom(12)).decode('utf-8')
            session['state'] = state
            discord_auth_uri = concate_discord_auth_uri_with_state(state)

            session['webhook_setting'] = {
                'is_nsfw': form.is_nsfw.data,
                'lang': form.language.data
            }

            return redirect(discord_auth_uri)

        flash(gettext("Form validation failed."), 'danger')
        return render_template("index.html", form=form, lang=str(locale))
