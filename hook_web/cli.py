import os
import pathlib
import sys
import time

import click
from figure_hook.database import PostgreSQLDB

module_dir = pathlib.Path(__file__).parent.resolve()


@click.group()
def main():
    pass


@main.group()
def babel():
    """pybabel command"""
    pass


@main.group()
def check():
    """connection checking tool"""
    pass


@babel.command('compile')
def babel_compile():
    """compile translations."""
    directory = f"{module_dir}/translations"
    os.system(f"pybabel compile -d {directory}")


@babel.command('init')
def babel_init():
    """initialize translations."""
    support_langs = ['ja', 'zh']
    for lang in support_langs:
        input_file = f"{module_dir}/messages.pot"
        output_dir = f"{module_dir}/translations"
        os.system(
            f"pybabel init -i {input_file} -d {output_dir} -l {lang}"
        )


@babel.command('update')
def babel_update():
    """update translations."""
    input_file = f"{module_dir}/messages.pot"
    directory = f"{module_dir}/translations"
    os.system(f"pybabel update -i {input_file} -d {directory}")


@babel.command('extract')
def babel_extract():
    """extract messages from source files and generate a POT file"""
    mapping_file = f"{module_dir}/babel.cfg"
    output_file = f"{module_dir}/messages.pot"
    os.system(
        f"pybabel extract -F {mapping_file} -k lazy_gettext -o {output_file} {module_dir}"
    )


@check.command('db')
def check_db():
    db = PostgreSQLDB()
    db_exist = False
    try_count = 0
    max_retry_times = 10
    interval = 1

    click.echo("Building database connection...")
    while not db_exist and try_count < max_retry_times:
        try:
            conn = db.engine.connect()
            conn.close()
            db_exist = True
            click.echo("Successfully build connection with database.")
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            click.echo(
                f"Failed to build connection with database. Retry after {interval} seconds. ({try_count + 1}/{max_retry_times})"
            )
            time.sleep(interval)
        finally:
            try_count += 1

    exit_code = 0 if db_exist else 1
    sys.exit(exit_code)


@check.command('redis')
def check_redis():
    from .config import Config
    redis = Config.SESSION_REDIS

    is_exist = False
    try_count = 0
    max_retry_times = 10

    click.echo("Building redis connection...")
    while not is_exist and try_count < max_retry_times:
        try:
            redis.ping()
            is_exist = True
            click.echo("Successfully build connection with redis.")
        except KeyboardInterrupt:
            raise click.exceptions.Abort
        except:
            click.echo(
                f"Failed to build connection with database. Retry... ({try_count + 1}/{max_retry_times})"
            )

        try_count += 1

    exit_code = 0 if is_exist else 1
    sys.exit(exit_code)


@main.command()
@click.option('-h', '--host', 'host', default="127.0.0.1", show_default=True)
@click.option('-p', '--port', 'port', type=int, default=8000, show_default=8000)
@click.option('--cert', 'cert_path', help="SSL cert file")
@click.option('--key', 'key_path', help="SSL key file")
def run(host, port, cert_path, key_path):
    from .app import create_app
    app = create_app()

    ssl_context = None
    if cert_path and key_path:
        ssl_context = (cert_path, key_path)

    app.run(host=host, port=port, ssl_context=ssl_context, load_dotenv=True)


if __name__ == '__main__':
    main()
