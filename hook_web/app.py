# -*- coding: utf-8 -*-
import os

from figure_hook.Models.base import Model
from flask import Flask, request

from .config import config
from .controllers import auth, public
from .extension import babel, cors, csrf, db, session


def create_app(config_name=os.environ.get("FLASK_ENV")):
    """App factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    register_context_callbacks(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_context_callbacks(app: Flask):
    @app.before_request
    def set_db_session():
        Model.set_session(db.session)

    @app.teardown_request
    def unset_db_session(response_or_exc):
        Model.set_session(None)


def register_extensions(app: Flask):
    """Register Flask extensions."""
    # login_manager.init_app(app)
    # oauth.init_app(app)
    session.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(['en', 'ja', 'zh'], default='en')


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.blueprint)
    app.register_blueprint(auth.blueprint)
