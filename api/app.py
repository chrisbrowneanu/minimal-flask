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
    return Response("VirtuousLoop is running! That info", status=200)


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

def default_var():
    d = {
        "pdf_ne": 'pdf_ne',
        "pdf_nw": 'pdf_nw',
        "pdf_h1_text": 'pdf_h1_text',
        "pdf_h2_text": 'pdf_h2_text',
        "pdf_p_text": 'pdf_p_text',
        "pdf_stylesheet": 'pdf_stylesheet',
        "record_title": 'record_title',
        "record_name": 'record_name',
        "record_user": 'record_user',
        "record_comment_a": 'record_comment_a'
    }
    return d

@app.route("/marks", methods = ['POST'])
def marks():
    """turns the marks json into css feedback"""
    loader = jinja2.FileSystemLoader(searchpath=template_path())
    env = jinja2.Environment(loader=loader)

    data_received = request.get_json()
    default_variables = default_var()
    variables =  default_variables | data_received

    template = env.get_template("feedback_marks.html")
    stylesheet = stylesheet_path(variables["pdf_stylesheet"])

    try:
        html_out = template.render(variables=variables)
        pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    except Exception:
        app.logger.debug("Exception on pdf_out")

    return Response(pdf_out, mimetype="application/pdf")
