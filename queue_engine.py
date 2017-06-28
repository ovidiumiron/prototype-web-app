"""
This files represents just a chuck of the work related with DB implementation.
The implementation is not done.
"""
from sqlalchemy import and_

from tempfile import NamedTemporaryFile

from image_utilities import get_type, image2memory
from db import db
from model import Image


def write(data):
    """
    Write image to DB.
    """
    img = Image(original=data)
    db.session.add(img)
    db.session.commit()
    return img.id


def read(id, prefix):
    """
    Read the image with id=id from DB and yield the path to the image.
    """
    image = db.session.query(Image).filter(and_(Image.text != None,
                                                Image.id == id)).first()
    if image:
        image_type = get_type(image2memory(image.original))
        file = NamedTemporaryFile(prefix=prefix,
                                  mode='w+b',
                                  suffix='.{0}'.format(image_type))
        file.write(image.text)
        file.seek(0, 0)
        return (file, image_type)
