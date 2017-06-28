from celery_factory import make_celery
from celery.exceptions import Ignore
from celery import states

from flask import Flask
import logging

from image_utilities import transformation, to_json


app = Flask(__name__)
app.config.from_object("config.DevConfig")

celery = make_celery(app)


@celery.task(name='worker.put_image')
def transformation_task(image):
    """
    Does the transformation of the image.
    But back into the message queue the result.
    If there is error change the status of the task to FAILURE.
    """
    try:
        return to_json(transformation(image).getbuffer().tobytes())
    except (OSError, TypeError) as e:
        logging.error("Task id: {0} raise exception: < {1} >"
                      "".format(transformation_task.request.id, e))
        transformation_task.update_state(state=states.FAILURE)
        raise Ignore()
