import os
import jinja2
from flask import Flask, Response, jsonify, request
from weasyprint import HTML
import logging
from os import walk



from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors, flush=True)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route("/")
def index():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return Response("Hello, Ubuntu!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route("/health")
def health():
    return Response("OK", status=200)


def template_path():
    app.logger.debug("template path")
    base = os.getcwd()
    app.logger.debug("base")
    app.logger.debug(base)
    path = os.path.join(base, "jinja", "templates")
    app.logger.debug("path")
    app.logger.debug(path)
    app.logger.debug("listdir")
    app.logger.debug(os.listdir())
    app.logger.debug("listdir-path")
    app.logger.debug(os.listdir(path))
    return path


def stylesheet_path(stylesheet):
    base = os.getcwd()
    path = os.path.join(base, "includes", "stylesheet", stylesheet)
    return path


@app.route("/marks")
def marks():
    """turns the marks json into stylesheet feedback"""
    app.logger.debug("running marks")
    loader = jinja2.FileSystemLoader(searchpath=template_path())
    env = jinja2.Environment(loader=loader)

    app.logger.debug("env")
    app.logger.debug(env)

    app.logger.debug("here's jinja")

    options = {
        "ne": "Course ABC",
        "nw": "XYZ",
        "h1_text": "Feedback for",
        "h2_text": "General comments",
        "p_text": "Feedback against criteria",
        "stylesheet": "single.css",
    }

    record = {
        "title": "Record Title",
        "name": "Record Name",
        "user": "Record User",
        "comment_a": "Comment A",
    }

    app.logger.debug("before template")
    template = env.get_template("feedback_marks.html")

    app.logger.debug("before stylesheet")
    stylesheet = stylesheet_path(options["stylesheet"])

    app.logger.debug("before try")

    try:
        app.logger.debug("during try")
        html_out = template.render(options=options, record=record, stylesheet=stylesheet)
        pdf_out = HTML(string=html_out).write_pdf()
    except Exception:
        app.logger.debug("during except")
        print("test", flush=True)

    app.logger.debug("before return")

    # return Response("trying marks...!", status=200)
    return Response(pdf_out, mimetype="application/pdf")
    # return Response(html_out, status=200)