import click
import datetime
import flask
import urllib

from .click import click_additional_options

_api_url = None
_frontend_url = None
_tus_url = None  # None means equal to _api_url


@click_additional_options
@click.option(
    "--api-url", help="BaNaNaS API URL.", default="https://api.bananas.openttd.org", show_default=True, metavar="URL",
)
@click.option(
    "--tus-url",
    help="Tus upload URL. Only set this, if different from API URL.",
    default=None,
    show_default=False,
    metavar="URL",
)
@click.option(
    "--frontend-url",
    help="Frontend URL (this server).",
    default="https://bananas.openttd.org",
    show_default=True,
    metavar="URL",
)
def click_urls(api_url, frontend_url, tus_url):
    global _api_url, _frontend_url, _tus_url
    _api_url = api_url
    _frontend_url = frontend_url
    _tus_url = tus_url


def template(*args, **kwargs):
    messages = kwargs.setdefault("messages", [])
    if "message" in kwargs:
        messages.append(kwargs["message"])
    if "message" in flask.request.args:
        messages.append(flask.request.args["message"])
    kwargs["copyyear"] = datetime.datetime.utcnow().year

    response = flask.make_response(flask.render_template(*args, **kwargs))
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


def external_url_for(*args, **kwargs):
    return _frontend_url + flask.url_for(*args, **kwargs)


def api_host():
    return _api_url


def tus_host():
    return _tus_url or _api_url


def tus_url():
    return urllib.parse.urljoin(tus_host(), "/new-package/tus/")


def redirect(*args, **kwargs):
    return flask.redirect(flask.url_for(*args, **kwargs))


def not_found():
    flask.abort(redirect("root", message="Data not found"))
