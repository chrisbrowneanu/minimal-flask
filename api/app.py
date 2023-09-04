from flask import Flask, Response, jsonify, request

from .errors import errors

app = Flask(__name__)
app.register_blueprint(errors)

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


@app.route('/marks')
def marks():
    '''turns the marks json into stylesheet feedback'''

    loader = jinja2.FileSystemLoader(searchpath=template_path())
    env = jinja2.Environment(loader=loader)

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

    template = env.get_template('feedback_marks.html')
    stylesheet = stylesheet_path(options['stylesheet'])

    try:
        html_out = template.render(options=options,
                                   record=record)
        pdf_out = HTML(string=html_out).write_pdf(stylesheets=[stylesheet])
    except Exception:
        print("test")

    return Response(pdf_out, mimetype="application/pdf")