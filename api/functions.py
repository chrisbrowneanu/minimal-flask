from flask import Blueprint
import os

functions = Blueprint("functions", __name__)


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
        "pdf_stylesheet": "single.css",
        "pdf_template": "feedback_marks.html",
        "pdf_ne": "",
        "pdf_nw": "",
        "pdf_se": "",
        "pdf_sw": "",
    }
    return d

