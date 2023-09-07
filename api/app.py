from flask import Flask, Response, jsonify, request
from weasyprint import HTML
import jinja2
import os


from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors, flush=True)

@app.route("/")
def index():
    return Response("Hello, it's running even better now!", status=200)


@app.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@app.route("/health")
def health():
    return Response("OK", status=200)


def template_path():
    print("template path", flush=True)
    base = os.getcwd()
    print("base", flush=True)
    print(base, flush=True)
    path = os.path.join(base, 'jinja', 'templates')
    return path

def stylesheet_path(stylesheet):
    base = os.getcwd()
    path = os.path.join(base, 'includes', 'stylesheet', stylesheet)
    return path

@app.route('/marks')
def marks():
    '''turns the marks json into stylesheet feedback'''

    print("running marks", flush=True)
    loader = jinja2.FileSystemLoader(searchpath=template_path())
    env = jinja2.Environment(loader=loader)

    print("env", flush=True)
    print(env, flush=True)

    print("here's jinja", flush=True)

    options = {
        'ne':"Course ABC",
        'nw':"XYZ",
        'h1_text':"Feedback for",
        'h2_text':"General comments",
        'p_text':"Feedback against criteria",
        'stylesheet':'single.css'
    }

    record = {
        'title':"Record Title",
        'name':"Record Name",
        'user':"Record User",
        'comment_a':"Comment A"
    }

    print("before template", flush=True)
    template = env.get_template('feedback_marks.html')


    print("before stylesheet", flush=True)
    stylesheet = stylesheet_path(options['stylesheet'])

    print("before try", flush=True)

    try:
        print("during try", flush=True)
        html_out = template.render(options=options,
                                   record=record)
        pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    except Exception:
        print("during except", flush=True)
        print("test", flush=True)

    print("before return", flush=True)
    return Response(pdf_out, mimetype="application/pdf")