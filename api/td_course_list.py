import jinja2
from flask import Blueprint, Response, request
from weasyprint import HTML
import unidecode
import api.functions as fn

# import pandas as pd
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from statistics import mean
import random
import csv
import os

td_course_list = Blueprint("td_course_list", __name__)

@td_course_list.route("/td", methods = ['GET','POST'])
def feedback_td_course_list():
    """turns the marks json into css feedback"""

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    with open('td_courses/td_data.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    # load the template
    template = env.get_template("td_courses.html")
    stylesheet = fn.stylesheet_path("single.css")

    cwd = os.getcwd()

    try:
        html_out = template.render(rows=rows, cwd=cwd)
        converted = html_out.encode('ascii',errors='ignore').decode('ascii')
        HTML(string=converted).write_pdf('td_courses/TD_Courses.pdf', stylesheets=[stylesheet])
    except Exception as e: print(e)

    return Response(converted, status=200)