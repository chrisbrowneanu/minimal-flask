import jinja2
from flask import Flask, Blueprint, Response, request, render_template, send_from_directory, url_for
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
from time import gmtime, strftime

td_course_list = Blueprint("td_course_list", __name__, static_folder='static', static_url_path='/static')

def open_csv(f):
    with open(f, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
        return rows

@td_course_list.route("/td", methods = ['GET','POST'])
def feedback_td_course_list():
    """turns the marks json into css feedback"""

    # load the jinja environment
    loader = jinja2.FileSystemLoader(searchpath=fn.template_path())
    env = jinja2.Environment(loader=loader)

    td_data = open_csv('td_courses/td_data.csv')
    td_master = open_csv('td_courses/td_master.csv')
    td_levels = open_csv('td_courses/td_levels.csv')
    td_elements = open_csv('td_courses/td_elements.csv')

    print('td_elements')
    print(td_elements)

    this_list = []
    for row in td_master:
        this_row = {
            'Course_Code': row['Course_Code'],
            'College': row['College'],
        }
        for data in td_data:
            if row['Course_Code'] == data['Course_Code']:
                this_data = {
                    'Course_Code': data['Course_Code'],
                    'Course_Name': data['Course_Name'],
                    'URL': data['URL'],
                    'Last_Assessed': data['Last_Assessed'],
                    'Last_Published': data['Last_Published'],
                    'Prerequisite_Courses': data['Prerequisite_Courses'],
                    'Prerequisite_Units': data['Prerequisite_Units'],
                }
                this_row.update(this_data)
                this_td_elements = []
                for element in td_elements:
                    this_level_description, this_class = "-", "blank"
                    for level in td_levels:
                        if level['td_element'] == element['td_element']:
                            if level['td_level'] == data[element['td_col']]:
                                this_level_description = level['td_level_description']
                                this_class = level['td_class']
                    this_element = {
                        'td_element': element['td_element'],
                        'td_title': element['td_title'],
                        'td_headline': element['td_headline'],
                        'td_description': element['td_description'],
                        'test_key': 'test_val',
                        'this_level': data[element['td_col']],
                        'this_level_written': data[str(element['td_col']) + '_Written'],
                        'this_level_description': this_level_description,
                        'this_class': this_class
                    }
                    this_td_elements.append(this_element)

                this_row.update({'td_elements': this_td_elements})
                print(this_row)
        this_list.append(this_row)

    template = env.get_template("td_courses.html")
    stylesheet = fn.stylesheet_path("single.css")

    current_date = strftime("%d-%b %Y", gmtime())
    print(current_date)

    try:
        html_out = template.render(td_rows=this_list, td_elements=td_elements, date=current_date)

        converted = html_out.encode('ascii',errors='ignore').decode('ascii')
        html_file = open('td_courses/td_courses.html', 'w')
        html_file.write(converted)
        html_file.close()

        HTML('td_courses/td_courses.html').write_pdf('td_courses/td_courses.pdf', stylesheets=[stylesheet])

    except Exception as e: print(e)

    return Response(converted, status=200)