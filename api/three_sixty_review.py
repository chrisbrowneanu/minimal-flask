import jinja2
from flask import Blueprint, Response, request
from weasyprint import HTML
import unidecode
import api.functions as fn

# import pandas as pd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import numpy as np

three_sixty_review = Blueprint("three_sixty_review", __name__)

@three_sixty_review.route("/three_sixty_review", methods = ['POST'])
def feedback_three_sixty_review():
    """turns the marks json into css feedback"""

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    # take the POST json, and merge it with the default variables needed in the template
    variables = request.get_json()
    chart = build_stripplot(variables)


    # load the template
    template = env.get_template("three_sixty_review.html")
    stylesheet = fn.stylesheet_path(variables['summary']['pdf_stylesheet'])

    # build the pdf
    try:
        html_out = template.render(variables=variables,
                               chart=chart)
        converted = html_out.encode('ascii',errors='ignore').decode('ascii')
        print("converted")
        print(converted)
        pdf_out = HTML(string=converted).write_pdf(stylesheets=[stylesheet])
    except Exception:
        converted = ""
        pdf_out = HTML(string=converted).write_pdf(stylesheets=[stylesheet])
        app.logger.debug("Exception on pdf_out")

    # return the pdf
    return Response(pdf_out, mimetype="application/pdf")


# def palette_roles_dict(dataframe):
#     '''assign the palette colours for each role'''
#     role_list = column_to_list(dataframe, 'role')
#     sorted_dict = {}
#     for k, v in cfg['roles_list'].items():
#         if v['title'] in role_list:
#             sorted_dict[v['title']] = v['palette']
#     return sorted_dict
#
def build_stripplot(variables):
#     '''stripplot with each crit and eye'''
#
    # palette_map = palette_roles_dict(dataframe)
    crit_labels = ["Working under supervision", "Communication/professionalism", "Analysis of data/information", "Critical-thinking/judgement"]

    sns.set(rc={'figure.figsize': (8, 3)})
    sns.set_style("ticks")

    # ax = sns.stripplot(x="", y="", data=df, hue='role', s=10, alpha=0.6, jitter=True, palette=palette_map)

    # tips = sns.load_dataset("tips")
    # ax = sns.stripplot(x="total_bill", data=tips, s=10, alpha=0.6, jitter=True)

    # Sample data
    df = pd.DataFrame(
        {
            'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
            'Value': [1, 2, -1, 0, -2, 2]
         }
    )
    # Create horizontal point plot
    ax = sns.stripplot(x='Value', y='Category', data=df, s=10, alpha=0.6, jitter=True)

    ax.set_xlabel("")
    ax.set_ylabel("")

    ax.set_xticks([-2,0,2])

    ax.set_xticklabels(["Well-below expectations", "About expectations" ,"Well-above expectations"], rotation=0, va="center")
    ax.set_yticklabels(crit_labels)

    ax.set_xlim([-2.5, 2.5])

    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)

    ax.grid(color='white', axis='x', linestyle='dotted', linewidth=0.1)
    ax.grid(color='gray', axis='y', linestyle='solid', linewidth=0.5)
    ax.tick_params(direction='inout', length=10, width=0.5, color='gray', pad=10)

    chartBox = ax.get_position()
    ax.set_position([0.3, 0.3, chartBox.width * 0.7, chartBox.height * 0.9])
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.4), ncol=3)

    # Save plot to StringIO
    from io import StringIO
    i = StringIO()
    plt.savefig(i, format="svg")
    # How to access the string
    fig = i.getvalue()

    return fig

#
# stripplot:
#   find_labels: ["Well-below expectations", "Below expectations", "About expectations", "Above expectations", "Well-above expectations"]
#   replace_values: [-2, -1, 0, 1, 2]
#   x_axis_title: 'Perceived performance'
#   y_axis_title: 'Criteria'
#   x_tick_values: [-2,-0,2]
#   x_tick_labels: ["Well-below expectations", "About expectations" ,"Well-above expectations"]
#   x_axis_lim: [-2.5, 2.5]
#   anon_legend: 'reviewer' # the anon label shown in the legend
#   colormap: 'viridis'
#
# stripplot_2:
#   x_axis_title: 'Perceived performance'
#   y_axis_title: 'Criteria'
#   x_tick_values: [-2,-0,2]
#   x_tick_labels: ["Well-below expectations", "About expectations" ,"Well-above expectations"]
#   x_axis_lim: [-2.5, 2.5]
#   anon_legend: 'reviewer' # the anon label shown in the legend
#   colormap: 'viridis'
#
#
# # order in roles_list determines comment print order
# # palette refers to colour in graph
# roles_list:
#   0:
#     title: "ANU Supervisor"
#     palette: "#FDE825"
#   1:
#     title: "Host Organisation Supervisor"
#     palette: "#3CBC76"
#   2:
#     title: "Student"
#     palette: "#3F4788"
#   3:
#     title: "Team Member"
#     palette: "#414487"
#   4:
#     title: "Shadow"
#     palette: "#2A788E"
#   5:
#     title: "Tutor"
#     palette: "#7AD151"
#   6:
#     title: "Client"
#     palette: "#22A884"
#   7:
#     title: "Average"
#     palette: "#FDE725"
