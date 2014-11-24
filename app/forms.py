from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class UploadForm(Form):
    filename = FileField('CSV File for Matrix', validators=[FileRequired(),FileAllowed(['.jpg', 'png', 'gif'], 'Images only, fool!')])
