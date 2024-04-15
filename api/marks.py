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
    variables = request.get_json()
    rubric = process_json(variables)

    # load the template
    template = env.get_template("feedback_marks.html")

    stylesheet = fn.stylesheet_path(variables["pdf_stylesheet"])
    print("here")
    # build the pdf
    # try:
    html_out = template.render(variables=variables,
                               rubric=rubric)
    print("html_out")
    print(html_out)
    pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    # except Exception:
    #     app.logger.debug("Exception on pdf_out")

    # return the pdf
    return Response(pdf_out, mimetype="application/pdf")

def process_json(variables):
    res = []
    for field_item in variables['fields']:
        if 'crit' in field_item['field']:
            rubric_levels = []
            for rubric_item in variables['rubric_levels']:
                if rubric_item['rubric'] == 'show':
                    for rubric_desc in variables['rubric_desc']:
                        if rubric_desc['field'] == field_item['field'] and rubric_desc['level'] == rubric_item['level']:
                            rubric_item.update({'description': rubric_desc['description']})
                    for k,v in variables['record'].items():
                        if k.lower() == field_item['field']:
                           for level_item_find in variables['rubric_levels']:
                               if v == level_item_find['level']:
                                   if level_item_find['class1'] == rubric_item['level'] and level_item_find['class2'] == rubric_item['level']:
                                       rubric_item.update({'background': 'b100'})
                                   elif level_item_find['class1'] == rubric_item['level'] or level_item_find['class2'] == rubric_item['level']:
                                       rubric_item.update({'background': 'b50'})
                                   else:
                                       rubric_item.update({'background': 'b0'})
                    rubric_levels.append(rubric_item)
            field_item.update({'rubric_levels': rubric_levels})
        res.append(field_item)
    return res
