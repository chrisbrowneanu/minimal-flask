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
import json
import csv
from csv import DictReader

sete_sessions = Blueprint("sete_sessions", __name__)

@sete_sessions.route("/sete", methods = ['GET', 'POST'])
def feedback_sete_sessions():
    """turns the marks json into css feedback"""

    print("here")

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    # take the POST json, and merge it with the default variables needed in the template

    # variables = request.get_json()

    with open('sete/data.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        variables = [row for row in reader]

    with open('sete/streams.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        streams = [row for row in reader]


    # load the template
    template = env.get_template("sete_sessions.html")
    stylesheet = fn.stylesheet_path("single.css")

    for stream in streams:
        try:
            html_out = template.render(variables=variables, stream=stream)
            converted = html_out.encode('ascii',errors='ignore').decode('ascii')
            HTML(string=converted).write_pdf('sete/' + stream['stream_title'] + '.pdf', stylesheets=[stylesheet])
        except Exception as e: print(e)

    return Response(converted, status=200)