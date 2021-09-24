from distutils.util import strtobool

from figure_hook.Models.base import Model
from flask import request, abort
from flask.helpers import make_response
from flask.templating import render_template
from flask_babel import get_locale

from .extension import db

__all__ = [
    "set_model_session",
]


def set_model_session():
    Model.set_session(db.session)
