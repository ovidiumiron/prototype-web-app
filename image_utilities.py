from PIL import Image, ImageFont, ImageDraw
from random import choice
from string import ascii_uppercase, digits
from time import strftime
from io import BytesIO


# CONSTANTS FOR TRANSFORMATION
SIZE_TEXT = 16
X_Y = (0, 0)
RGB = (0, 0, 0)


def random_generator(size=10, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for x in range(size))


def to_json(python_object):
    """ Represent the image to something which is JSON serializable. """
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': list(python_object)}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    """ Get bytes from image. """
    if '__class__' in json_object:
        if json_object['__class__'] == 'bytes':
            return bytes(json_object['__value__'])
    return json_object


def transformation(source):
    """ Return an BytesIO containing the transformed image. """
    img = Image.open(BytesIO(from_json(source)))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSerif.ttf", SIZE_TEXT)
    text = "{0} - {1}".format(strftime("%I:%M:%S"), random_generator())
    draw.text(X_Y, text, RGB, font=font)
    destination = BytesIO()
    img.save(destination, format=img.format)
    return destination


def is_valid_image(img):
    """ Check if can open the image and return the img as bytes class. """
    data = img.read()

    # Open the file to check if data is corrupted or not.
    # If the data is corrupted Image.open raise exception OSError
    Image.open(BytesIO(data))
    return data


def get_image_type(source):
    return Image.open(source).format
