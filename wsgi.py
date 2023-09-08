from api import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)