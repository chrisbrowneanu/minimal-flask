from flask import *
from jinja2 import Environment, PackageLoader



import api.functions as fn

views = Blueprint("views", __name__)
env = Environment(loader=PackageLoader('jinja'))


@views.route("/search")
def view_search():
    """view"""

    return render_template('search.html')