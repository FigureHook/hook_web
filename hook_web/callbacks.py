from figure_hook.Models.base import Model

from .extension import db

__all__ = [
    "set_model_session",
    "unset_model_session"
]


def set_model_session():
    Model.set_session(db.session)


def unset_model_session(response_or_exc):
    Model.set_session(None)
    return response_or_exc
