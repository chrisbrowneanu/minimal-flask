import jinja2
from flask import Blueprint, Response, request
from weasyprint import HTML
import unidecode
import api.functions as fn

three_sixty_review = Blueprint("three_sixty_review", __name__)

@three_sixty_review.route("/three_sixty_review", methods = ['POST'])
def feedback_three_sixty_review():
    """turns the marks json into css feedback"""

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    # take the POST json, and merge it with the default variables needed in the template
    variables = request.get_json()
    data = process_json(variables)

    # load the template
    template = env.get_template("three_sixty_review.html")

    stylesheet = fn.stylesheet_path(variables['summary']['pdf_stylesheet'])
    # build the pdf
    # try:
    html_out = template.render(variables=variables)

    converted = html_out.encode('ascii',errors='ignore').decode('ascii')
    # converted = unidecode.unidecode(html_out)

    pdf_out = HTML(string=converted).write_pdf(stylesheets=[stylesheet])
    # except Exception:
    #     app.logger.debug("Exception on pdf_out")

    # return the pdf
    return Response(pdf_out, mimetype="application/pdf")


def process_json(variables):
    records=[]
    for record in variables['records']:
        print(record)
    # res = []
    # for crit in variables['fields']:
    #     if 'crit' in crit['field']:
    #         row = []
    #         for col in variables['rubric_levels']:
    #             for cell in variables['rubric_desc']:
    #                 if 'crit' in crit['field'] and col['rubric'] == 'show' and crit['field'] == cell['field'] and col['level'] == cell['level']:
    #                     for k,v in variables['records'].items():
    #                         if k.lower() == crit['field']:
    #                             for level_item_find in variables['rubric_levels']:
    #                               if v == level_item_find['level']:
    #                                   if level_item_find['class1'] == col['level'] and level_item_find['class2'] == col['level']:
    #                                       background = 'b100'
    #                                   elif level_item_find['class1'] == col['level'] or level_item_find['class2'] == col['level']:
    #                                       background = 'b50'
    #                                   else:
    #                                       background = 'b0'
    #                     row.append({'level': cell['level'],
    #                                 'description': cell['description'],
    #                                 'background': background})
    #         crit['row'] = row
    #         res.append(crit)
    return res