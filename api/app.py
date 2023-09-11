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
    app.logger.debug('DEBUG logging')
    app.logger.info('INFO logging')
    return Response("VirtuousLoop is running! This_info", status=200)


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
    base = os.getcwd()
    path = os.path.join(base, "jinja", "templates")
    return path


def stylesheet_path(stylesheet):
    base = os.getcwd()
    path = os.path.join(base, "static", "css", stylesheet)
    return path


@app.route("/marks", methods=["PUT"])
def marks():
    """turns the marks json into css feedback"""
    loader = jinja2.FileSystemLoader(searchpath=template_path())
    env = jinja2.Environment(loader=loader)

    default_options = {
        "ne": "Course ABC",
        "nw": "XYZ",
        "h1_text": "Feedback for",
        "h2_text": "General comments",
        "p_text": "Feedback against criteria",
        "stylesheet": "single.css",
    }

    default_record = {
        "title": "Record Title",
        "name": "Record Name",
        "user": "Record User",
        "comment_a": "Comment A",
    }

    options = request.args.get('options', default_options)
    record = request.args.get('record', default_record)
    this_info = request.get_json()

    template = env.get_template("feedback_marks.html")
    stylesheet = stylesheet_path(options["stylesheet"])

    try:
        html_out = template.render(options=options, record=record, this_info=this_info)
        pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    except Exception:
        app.logger.debug("Exception on pdf_out")

    return Response(pdf_out, mimetype="application/pdf")
