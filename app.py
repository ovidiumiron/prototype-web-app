from celery import exceptions
from flask import Flask, request, render_template, send_file, jsonify, flash
from io import BytesIO
import logging
import requests

from celery_tasks import transformation_task
from image_utilities import is_valid_image, to_json, from_json, get_image_type


app = Flask(__name__)
app.config.from_object("config.DevConfig")


@app.route("/")
@app.route("/index")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    """
    url = "http://{0}:{1}/image".format(
        app.config["HOST_NAME"], app.config["PORT"])
    resp_put = requests.post(url, files=request.files)

    status_code = resp_put.status_code
    if status_code == 400:
        flash("Image bad format. Try with other file.")
        return render_template("upload.html")
    elif status_code == 500:
        flash("Server probleme....Try again.")
        return render_template("upload.html")
    elif status_code == 200:
        flash("It's time to hit the button!")
        return render_template("upload.html", id=resp_put.json()['id'])
    else:
        flash("Server problem....Try again.")
        app.logger.error("unexpected status_code: {0} from REST API"
                         "".format(status_code))
        return render_template("upload.html")


@app.route('/image', methods=["POST"])
def put_image():
    """
    REST API ENDPOINT:   '/image'

    Put image in message queue.
    Method: POST
    Input:  request.file['image'] - image to save in message queue
    Return: the id of the task if success or error code other.
    """
    if 'image' not in request.files:
        return jsonify(), 400
    image = request.files['image']

    try:
        data = is_valid_image(image.stream)
    except (OSError, ValueError) as e:
        return jsonify(), 400

    try:
        task = transformation_task.delay(to_json(data))
    except (exceptions.CeleryError, TypeError) as e:
        app.logger.error(e)
        return jsonify(), 500

    app.logger.info("put task id:{0}".format(task.id))
    return jsonify(id=task.id), 200


@app.route('/image/<id>', methods=["GET", "POST"])
def get_image(id):
    """
    REST API ENDPOINT:   '/image'

    Get image in message queue.
    Method: GET
    Input:  id - the id of the message from queue
    Return: the image if success or error code other
    """
    task = transformation_task.AsyncResult(id)

    if task.status == "FAILURE":
        flash("Server error. Try to upload other image")
        return jsonify(), 500
    elif task.status == "SUCCESS":
        image = from_json(task.get())
        try:
            return send_file(BytesIO(image),
                             mimetype=get_image_type(BytesIO(image)))
        except OSError:
            flash("Server error. Try to upload other image")
            return jsonify(), 500
    else:
        flash("Not ready. Try again.")
        return jsonify(), 204


if __name__ == "__main__":
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(app.config["HOST_NAME"],
            app.config["PORT"],
            app.config["USE_RELOADER"],
            threaded=app.config["THREADED"],
            processes=app.config["PROCESSES"])
