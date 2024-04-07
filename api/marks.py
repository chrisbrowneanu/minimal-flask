import jinja2
from flask import Blueprint, Response, request
from weasyprint import HTML

import api.functions as fn

marks = Blueprint("marks", __name__)

@marks.route("/marks", methods = ['POST'])
def feedback_marks():
    """turns the marks json into css feedback"""

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    # take the POST json, and merge it with the default variables needed in the template
    post_json = request.get_json()
    default_variables = fn.default_var()
    variables =  default_variables | post_json

    # load the template
    template = env.get_template("feedback_marks.html")
    stylesheet = fn.stylesheet_path(variables["pdf_stylesheet"])

    # build the pdf
    try:
        html_out = template.render(
            variables=variables,
            results=variables['results']
        )
        pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    except Exception:
        app.logger.debug("Exception on pdf_out")

    # return the pdf
    return Response(pdf_out, mimetype="application/pdf")