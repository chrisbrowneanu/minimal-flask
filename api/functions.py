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
        "pdf_ne": "NE",
        "pdf_nw": "NW",
        "pdf_se": "",
        "pdf_sw": "",
        "pdf_header": "Header",
        "pdf_description": "Description",
        "pdf_header_a": "Paragraph",
        "pdf_header_b": "",
        "pdf_header_c": "",
        "record_header": "Header",
        "record_text_a": "Comment A",
        "record_text_b": "",
        "record_text_c": ""
    }
    return d

