"""
This files represents just a chuck of the work related with DB implementation.
The implementation is not done.
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.DevConfig")
db = SQLAlchemy(app)
